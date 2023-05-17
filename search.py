import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search

from constants import EMBEDDING_MODEL
from constants import GPT_MODEL
from constants import OPENAI_API_KEY

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# ********* 1. Prepare search data *********

def get_embeddings(embeddings_path):
    df = pd.read_csv(embeddings_path)

    # convert embeddings from CSV str type back to list type
    df['embedding'] = df['embedding'].apply(ast.literal_eval)

    # the dataframe has two columns: "text" and "embedding"
    return df


# ********* 2. Search *********
"""
Takes a user query and a dataframe with text & embedding columns
Embeds the user query with the OpenAI API
Uses distance between query embedding and text embeddings to rank the texts
Returns two lists:
- The top N texts, ranked by relevance
- Their corresponding relevance scores
"""
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


# ********* 3. Ask *********

def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = 'Answer the question as truthfully as possible using the provided context.\n'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'{string}\n'
        if (
            num_tokens(message + next_article + question, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
    return message + question

"""
Takes a user query
Searches for text relevant to the query
Stuffs that text into a message for GPT
Sends the message to GPT
Returns GPT's answer
"""
def ask(
    query: str,
    df: pd.DataFrame,
    model: str = GPT_MODEL,
    token_budget: int = 2048 - 500,
    print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    # messages = [
    #     {"role": "system", "content": "You answer questions."},
    #     {"role": "user", "content": message},
    # ]
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=messages,
    #     temperature=0
    # )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message}",
        max_tokens=2048 - 500,
        n=1,
        stop=None,
        temperature=0,
    )
    response_message = response.choices[0].text.strip()
    if print_message:
        print(response_message)
    return response_message


def main():
    print('Running search.py...')

    embeddings_path = "data/embeddings.csv"
    df = get_embeddings(embeddings_path)

    while True:
        query = input('> ')
        ask(query=query, df=df, print_message=True)

if __name__ == '__main__':
    main()