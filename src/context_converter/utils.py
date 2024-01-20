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


async def save_checkpoint(file_path, chunk_id):
    """
    Saves the checkpoint of a given chunk ID to a file.

    Args:
        file_path (str): The path to the file where the checkpoint will be saved.
        chunk_id (int): The ID of the chunk to be saved as the checkpoint.

    Returns:
        None
    """
    try:
        async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
            await file.write(str(chunk_id))
            logging.info("Saved checkpoint: %s", chunk_id)
    except Exception as e:
        logging.error("Error saving checkpoint: %s", e)


async def save_output_in_chunks(file_path, contents, chunk_id):
    """
    Save the given content into a file in chunks.
    Also logs the chunk id to a separate log file.
    """
    try:
        async with aiofiles.open(file_path, "a", encoding="utf-8") as file:
            await file.write(contents)
            await file.flush()
            logging.info("Flushed file content: %s", file_path)

        # Log the chunk id to a separate log file
        async with aiofiles.open("progress.log", "a", encoding="utf-8") as log_file:
            await log_file.write(f"{chunk_id}\n")
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
