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
import aiofiles
import asyncio
from typing import List
from converter import HTMLToMarkdownConverter
from formatter import DatasetFormatter
from utils import load_json_files, save_output_in_chunks, chunk_dataset, save_output_in_chunks, save_checkpoint


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
    checkpoint_file: str = "checkpoint.txt",
) -> None:
    """
    Asynchronous function that performs the main execution logic of the program.

    Parameters:
    - `pattern` (str): The pattern to match for input files. Defaults to "output*.json".
    - `chunk_size` (int): The size of each data chunk. Defaults to 512.
    - `output_file_name` (str): The name of the output file. Defaults to "gpt-crawler-curated_markdown.md".
    - `checkpoint_file` (str): The name of the checkpoint file. Defaults to "checkpoint.txt".

    Returns:
    - None: This function does not return any value.
    """
    logging.basicConfig(level=logging.INFO)

    try:
        original_data = await load_json_files(pattern)
        chunks = list(chunk_dataset(original_data, chunk_size))

        # Read the checkpoint file
        last_processed_chunk = -1
        try:
            async with aiofiles.open(checkpoint_file, "r", encoding="utf-8") as file:
                last_processed_chunk = int(await file.read())
        except (FileNotFoundError, ValueError):
            pass  # No checkpoint file found or invalid content, start from the beginning

        for i, chunk in enumerate(chunks):
            if i <= last_processed_chunk:
                logging.info(
                    "Skipping chunk %d because it has already been processed", i
                )
                continue

            try:
                content = await process_dataset_chunk(chunk)
                await save_output_in_chunks(output_file_name, content, i)
                await save_checkpoint(checkpoint_file, i)
                logging.info("Processed and saved chunk %d", i)
            except Exception as e:
                logging.error("An error occurred while processing a chunk: %s", e)
                break  # Stop processing on error
    except Exception as e:
        logging.error("An error occurred in the main function: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
