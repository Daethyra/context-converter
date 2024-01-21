"""
This script defines a class HTMLToMarkdownConverter that is responsible for converting HTML content to Markdown format and processing text embeddings. It uses the transformers library to load a pretrained model for generating embeddings, and the beautifulsoup4 and markdownify libraries to parse and convert HTML content to Markdown. The class also includes methods for removing redundant data based on semantic similarity, and for curating the HTML content by removing specified elements and tags.
"""

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from transformers import AutoTokenizer, AutoModel
import torch
import logging


class HTMLToMarkdownConverter:
    def __init__(self, strip_tags=None, convert_links=True):
        """
        Initializes the object with optional parameters.

        Args:
            strip_tags (list): List of tags to strip from the text. Defaults to ["script", "style", "meta"].
            convert_links (bool): Flag to indicate whether to convert links. Defaults to True.

        Returns:
            None
        """
        self.strip_tags = strip_tags or ["script", "style", "meta"]
        self.convert_links = convert_links
        self.tokenizer, self.model = self._initialize_embedding_model()

    def _initialize_embedding_model(self):
        """
        Initializes the embedding model by loading the tokenizer and model from the "jinaai/jina-embeddings-v2-small-en" 
        pretrained checkpoints. Returns the initialized tokenizer and model.
        """
        tokenizer = AutoTokenizer.from_pretrained(
            "jinaai/jina-embeddings-v2-small-en", trust_remote_code=True
        )
        model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-small-en")
        return tokenizer, model

    def mean_pooling(self, model_output, attention_mask):
        """
        Perform mean pooling on the token embeddings based on the attention mask.

        Args:
            model_output (torch.Tensor): The output of the model.
            attention_mask (torch.Tensor): The attention mask.

        Returns:
            torch.Tensor: The result of mean pooling.
        """
        token_embeddings = model_output[0]
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def _process_embeddings(self, lines, batch_size=16):
        """
        Process embeddings for the given lines using batch processing.

        Args:
            lines (list): The list of input lines for which embeddings need to be processed.
            batch_size (int, optional): The size of each batch for processing. Defaults to 16.

        Returns:
            torch.Tensor: Normalized batched embeddings.
        """
        batched_embeddings = []
        for i in range(0, len(lines), batch_size):
            batch = lines[i : i + batch_size]
            encoded_input = self.tokenizer(
                batch, padding=True, truncation=True, return_tensors="pt"
            )
            with torch.no_grad():
                model_output = self.model(**encoded_input)
            batch_embeddings = self.mean_pooling(
                model_output, encoded_input["attention_mask"]
            )
            batched_embeddings.extend(batch_embeddings)

        return torch.nn.functional.normalize(
            torch.stack(batched_embeddings), p=2, dim=1
        )

    def _remove_redundant_data(self, embeddings, lines):
        """
        Remove redundant data from a list of lines based on cosine similarity between consecutive embeddings.

        Parameters:
            embeddings (torch.Tensor): A tensor of embeddings.
            lines (List[str]): A list of strings representing lines of text.

        Returns:
            str: A string representing the cleaned lines of text with redundant data removed.
        """
        cleaned_lines = [lines[0]]  # Always include the first line
        for i in range(1, len(lines)):
            similarity = torch.cosine_similarity(
                embeddings[i].unsqueeze(0), embeddings[i - 1].unsqueeze(0)
            )
            if similarity.item() < 0.86899:  # Threshold for redundancy
                cleaned_lines.append(lines[i])
        return "\n".join(cleaned_lines)

    def convert(self, html_content):
        """
        Convert the given HTML content to markdown format.

        Args:
            html_content (str): The HTML content to be converted.

        Returns:
            list: The processed embeddings with redundant data removed.
        Raises:
            Exception: If an error occurs during the conversion process.
        """
        try:
            curated_html = self._curate_content(html_content)
            markdown_content = md(
                curated_html,
                strip_tags=self.strip_tags,
                convert_links=self.convert_links,
            ).strip()
            lines = markdown_content.split("\n")
            embeddings = self._process_embeddings(lines)
            return self._remove_redundant_data(embeddings, lines)
        except Exception as e:
            logging.error("Error during conversion: %s", e)
            raise

    def _curate_content(self, html):
        """
        Curates the HTML content by parsing it with BeautifulSoup, removing selectors, 
        and stripping tags. Returns the curated HTML content as a string. 
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            self._remove_selectors(soup)
            self._strip_tags(soup)
            return str(soup)
        except Exception as e:
            logging.error("Error in curating HTML content: %s", e)
            return html

    def _remove_selectors(self, soup):
        """
        Remove specified selectors from the given BeautifulSoup object.

        Parameters:
        - soup: the BeautifulSoup object to remove selectors from (BeautifulSoup)

        Returns:
        - None
        """
        selectors = [
            "header",
            "footer",
            "nav",
            ".navbar",
            ".menu",
            ".footer-links",
            "#sidebar",
            "#ad-container",
            'div[class*="cookie"], div[class*="banner"]',
            "aside",
            ".pagination",
            "form",
        ]
        for selector in selectors:
            for element in soup.select(selector):
                element.decompose()

    def _strip_tags(self, soup):
        """
        Strip specified tags from the given BeautifulSoup object.

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object to strip tags from.

        Returns:
            None
        """
        for tag in self.strip_tags:
            for s in soup(tag):
                s.decompose()
