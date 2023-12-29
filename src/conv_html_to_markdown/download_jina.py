"""
This module is responsible for downloading the Jina library, which is used for processing text embeddings in the HTML to Markdown conversion project.

It uses the transformers library to download the Jina embeddings model and tokenizer. The model and tokenizer are then used in other parts of the project to process text embeddings.

The module contains the following components:
    - AutoTokenizer: Used to tokenize the text data.
    - AutoModel: Used to create the Jina embeddings model.
"""


from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained(
    "jinaai/jina-embeddings-v2-small-en", trust_remote_code=True
)
model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-small-en")
