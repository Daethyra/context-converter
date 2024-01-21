import glob
import json
import logging
import aiofiles
import asyncio
from converter import HTMLToMarkdownConverter
from formatter import DatasetFormatter


async def load_json_files(pattern):
    """
    Asynchronously loads JSON files matching the given pattern and aggregates their data.

    Args:
        pattern (str): The pattern to match JSON files.

    Returns:
        list: The aggregated data from the JSON files, or an empty list if an error occurs.
    """
    try:
        aggregated_data = []
        for file_path in glob.glob(pattern):
            async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
                data = await file.read()
                aggregated_data.extend(json.loads(data))
        return aggregated_data
    except Exception as e:
        logging.error("Error loading JSON files: %s", e)
        return []


async def save_output_in_chunks(file_path, contents):
    """
    Asynchronously saves the given contents to the specified file path in chunks.

    Args:
        file_path (str): The path of the file to save the contents to.
        contents (str): The contents to be saved to the file.

    Returns:
        None
    """
    try:
        async with aiofiles.open(file_path, "a", encoding="utf-8") as file:
            await file.write(contents)
            await file.flush()
            logging.info("Flushed file content: %s", file_path)
    except Exception as e:
        logging.error("Error saving output in chunks: %s", e)


def chunk_dataset(data, chunk_size):
    """
    Function to chunk a dataset into smaller parts based on the given chunk size.

    Args:
        data: The dataset to be chunked.
        chunk_size: The size of each chunk.

    Yields:
        The chunks of the dataset based on the chunk size.

    Returns:
        An empty list if an exception is caught during chunking.
    """
    try:
        for i in range(0, len(data), chunk_size):
            yield data[i : i + chunk_size]
    except Exception as e:
        logging.error("Error chunking dataset: %s", e)
        return []


def process_chunk(chunk):
    """
    Process a chunk using a DatasetFormatter and return the formatted dataset.
    If an exception occurs, log an error and return an empty string.
    """
    try:
        formatter = DatasetFormatter(HTMLToMarkdownConverter())
        return formatter.format_dataset(chunk)
    except Exception as e:
        logging.error("Error processing chunk: %s", e)
        return ""
