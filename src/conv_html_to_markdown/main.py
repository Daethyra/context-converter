"""
This module serves as the main entry point for the HTML to Markdown conversion project.

It contains the main function which loads, processes, and saves the dataset. The processing involves converting HTML content to Markdown and formatting it into a structured form. The dataset is processed in chunks to optimize memory usage and performance.

The module also includes functions for processing individual chunks of the dataset and for processing and collecting data from all chunks in parallel using multithreading.

Functions:
    process_dataset_chunk(chunk): Processes a single chunk of the dataset.
    main(): Main function to load, process, and save the dataset.
"""


import logging
from typing import List
import asyncio
from typing import List
from .converter import HTMLToMarkdownConverter
from .formatter import DatasetFormatter
from .utils import load_json_files, save_output_in_chunks, chunk_dataset


def process_dataset_chunk(chunk):
    """
    Processes a single chunk of the dataset.
    """
    try:
        formatter = DatasetFormatter(HTMLToMarkdownConverter())
        return formatter.format_dataset(chunk)
    except Exception as e:
        logging.error("Error processing dataset chunk: %s", e)
        return ""


async def main(
    pattern: str = "output*.json",
    chunk_size: int = 512,
    output_file_name: str = "gpt-crawler-curated_markdown.md",
) -> None:
    """
    Main function to load, process, and save the dataset.

    :param pattern: Pattern to match JSON files.
    :param chunk_size: Size of chunks to split the dataset into.
    :param output_file_name: Name of the output file.
    """
    logging.basicConfig(level=logging.INFO)

    try:
        original_data = await load_json_files(pattern)

        chunks = list(chunk_dataset(original_data, chunk_size))

        for chunk in chunks:
            try:
                content = await process_dataset_chunk(chunk)
                await save_output_in_chunks(output_file_name, content)
                logging.info("Conversion process successful. Exiting program.")
            except Exception as e:
                logging.error("An error occurred while processing a chunk: %s", e)
                # Handle error or save progress here
    except Exception as e:
        logging.error("An error occurred in the main function: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
