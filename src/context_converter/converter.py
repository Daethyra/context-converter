

from bs4 import BeautifulSoup
from markdownify import markdownify as md
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
