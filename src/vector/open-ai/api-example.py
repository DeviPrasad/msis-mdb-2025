"""
$ python3.11 -m venv ~/teaching/openai/
$ source ~/teaching/openai/bin/activate
$ cd ~/teaching/openai/
$ python3.11 -m pip install --upgrade pip
    pip-25.0.1
$ pip install tiktoken
    tiktoken-0.9.0
$ pip install openai
    openai-1.66.3
"""

import tiktoken

tt_ex_sentence = "This is an example sentence used to demonstrate OpenAI tokenization and embeddings API, in a BDA-2025-class!"


# https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
# cl100k_base in most cases - text-embedding-3-small, text-embedding-3-large, gpt-4
# o200k_base for gpt-4o and gpt-4o-mini
def tiktoken_encoding_for_model(model_name):
    return tiktoken.encoding_for_model(model_name)


def tokenize(model_name, text):
    encoding = tiktoken_encoding_for_model(model_name)
    return enc.encode(text)


if __name__ == "__main__":
    assert tiktoken_encoding_for_model("text-embedding-3-small") == "cl100k_base"

    tokens = tokenize("text-embedding-3-small", tt_ex_sentence)
    print(tokens)
