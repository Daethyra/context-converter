import unittest
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from transformers import AutoTokenizer, AutoModel
import torch
import logging
import os
import sys

# Get the absolute path of the parent directory
parent_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the system path
sys.path.append(parent_dir)

from conv_html_to_markdown.converter import HTMLToMarkdownConverter


class HTMLToMarkdownConverterTest(unittest.TestCase):
    def setUp(self):
        self.converter = HTMLToMarkdownConverter()

    def test_initialize_embedding_model(self):
        tokenizer, model = self.converter._initialize_embedding_model()
        # Call a method on each object and assert that it behaves as expected
        # For example:
        tokens = tokenizer.encode("Hello world", return_tensors="pt")
        self.assertIsInstance(tokens, torch.Tensor)
        outputs = model(tokens)
        self.assertIsInstance(outputs.last_hidden_state, torch.Tensor)

    def test_curate_content(self):
        html = '<html><head></head><body><div class="cookie">Cookie</div></body></html>'
        expected_html = "<html><head></head><body></body></html>"
        curated_html = self.converter._curate_content(html)
        self.assertEqual(curated_html, expected_html)

    def test_remove_selectors(self):
        html = "<html><head></head><body><header>Header</header></body></html>"
        expected_html = "<html><head></head><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        self.converter._remove_selectors(soup)
        self.assertEqual(str(soup), expected_html)

    def test_strip_tags(self):
        html = "<html><head></head><body><script>Script</script></body></html>"
        expected_html = "<html><head></head><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        self.converter._strip_tags(soup)
        self.assertEqual(str(soup), expected_html)

    def test_convert(self):
        html = "<html><head></head><body><p>Hello World!</p></body></html>"
        expected_markdown = "Hello World!"
        markdown_content = self.converter.convert(html)
        self.assertEqual(markdown_content, expected_markdown)


if __name__ == "__main__":
    unittest.main()
