# Convert and Format HTML to Markdown

## Purpose

For converting HTML to Markdown and formatting a dataset of HTML content 
into structured Markdown, with added capabilities of processing text embeddings to identify and remove redundant content.

* No API keys required
-> Because this project uses the open-source Jina Embeddings model locally, it's totally free to use.

## Installation & Setup

First clone the package: `git clone https://github.com/daethyra/conv_html_to_markdown.git`

To get started, run:

`pip install conv_html_to_markdown`

* Run `jina_embeddings.py` to preemptively download the embeddings model.

**Example integration**:

* Please see an example usage in [gpt-crawler](https://github.com/Daethyra/gpt-crawler). This fork of `gpt-crawler` has the `conv_html_to_markdown` package integrated into its processing pipeline. 

**Configuration**:
* You can clone the package repository to configure similarity threshold for removing content, chunk size, maximum number of threads, the file pattern to match when loading files for conversion, and the output file's name.

To do so, edit the parameter values passed into the `main` function in [main.py](./src/conv_html_to_markdown/main.py#async_def_main).