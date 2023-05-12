# imports
import numpy as np
import pandas as pd  # for DataFrames to store article sections and embeddings
import tiktoken  # for counting tokens
import openai  # for generating embeddings
from itertools import islice
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type


EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'
OPENAI_API_KEY = "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"


# let's make sure to not retry on an invalid request, because that is what we want to demonstrate
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6), retry=retry_if_not_exception_type(openai.InvalidRequestError))
def get_embedding(text_or_tokens, model=EMBEDDING_MODEL):
    return openai.Embedding.create(input=text_or_tokens, model=model)["data"][0]["embedding"]


def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := tuple(islice(it, n))):
        yield batch


def chunked_tokens(text, encoding_name, chunk_length):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    chunks_iterator = batched(tokens, chunk_length)
    yield from chunks_iterator


def len_safe_get_embedding(text, model=EMBEDDING_MODEL, max_tokens=EMBEDDING_CTX_LENGTH, encoding_name=EMBEDDING_ENCODING):
    chunk_embeddings = []
    for chunk in chunked_tokens(text, encoding_name=encoding_name, chunk_length=max_tokens):
        chunk_embeddings.append(get_embedding(chunk, model=model))
    return chunk_embeddings

def get_embeddings(chunks, model=EMBEDDING_MODEL, max_tokens=EMBEDDING_CTX_LENGTH, encoding_name=EMBEDDING_ENCODING):
    chunk_embeddings = []
    for chunk in chunks:
        chunk_embeddings.append(get_embedding(chunk, model=model))
    return chunk_embeddings


def main():
    print('Running embeddings.py...')

    # OpenAI API
    openai.api_key = OPENAI_API_KEY

    with open('data/knowledge_base.txt', 'r') as file:
        knowledge_base_text = file.read()
    
    knowledge_base_strings = knowledge_base_text.split('\n\n')
    embeddings = get_embeddings(knowledge_base_strings)

    df = pd.DataFrame({"text": knowledge_base_strings, "embedding": embeddings})

    embeddings_save_path = "data/embeddings.csv"
    df.to_csv(embeddings_save_path, index=False)

    print('Finished generating embeddings')

if __name__ == '__main__':
    main()


