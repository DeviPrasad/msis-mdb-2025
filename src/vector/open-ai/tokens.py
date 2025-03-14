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

"""
New embedding models and API updates - January 25, 2024
https://openai.com/index/new-embedding-models-and-api-updates/
"""

import tiktoken


what_is_this = """
def what_does_this_do_01(x):
    if x % 2 == 0:
        return true
    else:
        return false
"""


def encoder_for_model(model_name):
    """
    https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    cl100k_base: text-embedding-3-small, text-embedding-3-large, gpt-4.
    o200k_base: gpt-4o and gpt-4o-mini.
    """
    return tiktoken.encoding_for_model(model_name)


def tokenize(enc, text):
    return enc.encode(text)


def tokenize_simple_text():
    # change 'D' to 'd' in the second part of the sentence, and observe the difference in the output tokens.
    text = "This is an example sentence used for demonstrating tokenization. Mar-2025/BDA/Modern Databases for Big Data [BDA 5202]"

    enc = encoder_for_model("text-embedding-3-large")
    assert enc.name == "cl100k_base"

    token_ids = tokenize(enc, text)
    token_bytes = [enc.decode_single_token_bytes(tid) for tid in token_ids]
    assert len(token_ids) == len(token_bytes)

    # print(token_bytes)
    # print(token_ids)


def tokenize_loop_text():
    is_this_a_loop = """
    def what_does_this_do_02(x):
        import math
        if not (isinstance(x, int) and x > 1):
            raise Exception("bad argument")
        if x == 2:
            return (True, 2, "even")
        if x % 2 == 0:
            return (False, 2, "")
        sqrt_x = math.floor(math.sqrt(x))
        for d in range(2, sqrt_x):
            if x % d == 0:
                return (False, d, "")
        return (True, 0, "odd")
    """
    enc = encoder_for_model("text-embedding-3-large")
    assert enc.name == "cl100k_base"

    token_ids = tokenize(enc, is_this_a_loop)

    assert enc.decode(token_ids) == is_this_a_loop
    print(f"number of tokens = {len(token_ids)}")
    # print(token_ids)
    # print(enc.decode(token_ids))


if __name__ == "__main__":
    tokenize_simple_text()
    tokenize_loop_text()
