import asynctest
import os
import sys

# Get the absolute path of the parent directory
parent_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the system path
sys.path.append(parent_dir)

from conv_html_to_markdown.converter import HTMLToMarkdownConverter
from conv_html_to_markdown.formatter import DatasetFormatter


class TestDatasetFormatter(asynctest.TestCase):
    def setUp(self):
        self.converter = HTMLToMarkdownConverter()
        self.formatter = DatasetFormatter(self.converter)

    async def test_format_entry(self):
        entry = {
            "title": "Test Title",
            "url": "https://example.com/test-title",
            "html": "<p>This is a test.</p>",
        }
        expected_markdown = "## Test Title\n\n[Read More](https://example.com/test-title)\n\nThis is a test."
        # Use 'await' to wait for the coroutine to finish and get the result
        result = await self.formatter.format_entry(entry)
        self.assertEqual(result, expected_markdown)

    def test_structure_markdown(self):
        title = "Test Title"
        url = "https://example.com/test-title"
        content = "This is a test."
        expected_markdown = "## Test Title\n\n[Read More](https://example.com/test-title)\n\nThis is a test."
        self.assertEqual(
            self.formatter.structure_markdown(title, url, content), expected_markdown
        )

    async def test_format_dataset(self):
        data = [
            {
                "title": "Test Title 1",
                "url": "https://example.com/test-title-1",
                "html": "<p>This is a test 1.</p>",
            },
            {
                "title": "Test Title 2",
                "url": "https://example.com/test-title-2",
                "html": "<p>This is a test 2.</p>",
            },
        ]
        expected_markdown = "## Test Title 1\n\n[Read More](https://example.com/test-title-1)\n\nThis is a test 1.\n\n## Test Title 2\n\n[Read More](https://example.com/test-title-2)\n\nThis is a test 2."
        # Use 'await' to wait for the coroutine to finish and get the result
        result = await self.formatter.format_dataset(data)
        self.assertEqual(result, expected_markdown)


if __name__ == "__main__":
    asynctest.main()
