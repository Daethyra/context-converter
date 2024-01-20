import glob
import json
import logging
import aiofiles
import asyncio
from converter import HTMLToMarkdownConverter
from formatter import DatasetFormatter


async def load_json_files(pattern):
    """
    Load data from multiple JSON files matching a pattern.
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
    Save the given content into a file in chunks.
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
    Yields chunks of the dataset for processing.
    """
    try:
        for i in range(0, len(data), chunk_size):
            yield data[i : i + chunk_size]
    except Exception as e:
        logging.error("Error chunking dataset: %s", e)
        return []


def process_chunk(chunk):
    """
    Processes a single chunk of the dataset.
    """
    try:
        formatter = DatasetFormatter(HTMLToMarkdownConverter())
        return formatter.format_dataset(chunk)
    except Exception as e:
        logging.error("Error processing chunk: %s", e)
        return ""
