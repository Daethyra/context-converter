# Convert and Format HTML to Markdown

**Table of Contents**:

* [Description](#description)
* [Problem to Solve](#problem-to-solve)
* [Quick Start | Getting Started](#quick-start--getting-started)
* [Configuration](#configuration)

## Description

Extracts HTML content from a JSON file to produce a Markdown file. Leverages similarity threshold to remove redundant content.

## Problem to Solve

Building retrieval augmented generation AI applications can be a lengthy process. While there are web crawlers to collect content, the post processing of this content is equally important for accurate and helpful generation.

This library was built specifically to augment the [context-curator](https://github.com/Daethyra/context-curator) project by further automating the document creation process.

## Quick Start | Getting Started

1. Installation

* To have access to the package in your local environment, clone the repository using `git`: 
`git clone https://github.com/daethyra/context-converter.git`

* To install via pip, run: `pip install context-converter`

*Optional*: Run `jina_embeddings.py` to preemptively download the embeddings model.

2. Navigate into the `context-converter` folder: `cd context-converter`

3. Place a JSON file of HTML content into the same folder.

4. Run `python3 main.py`

Your output file will be created in the same folder.


## Configuration
You can tweak the similarity threshold and more to help yourself curate what you want.

i. In [main.py](./src/context_converter/main.py), you can set the following parameters to optimize your results:
* `main.py`
    * chunk_size: The size of the chunk to be processed. The default value is 256.
    * You can find speed tests [here](./.github/public/runtime-speed-test-results.txt "Speed test results").

ii. In [converter.py](./src/context_converter/converter.py), you can set the following parameters to optimize your results:
* `converter.py`
    * `similarity.item()`: The similarity threshold. The default value is 0.868899. Only similarity values above the threshold are removed, meaning a higher threshold removes *less* content. A lower threshold removes *more* content.
    * `batch_size`: Proccess embeddings for the given lines using batch processing. The default value is 16, which has proved to be faster than higher values, up to 256. [Speed test results](./.github/public/runtime-speed-test-results.txt "Speed test results").

## License
[MIT](./LICENSE)