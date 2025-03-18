"""
$ cd ~/teaching/openai/
$ source ./bin/activate
https://platform.openai.com/api-keys

Before starting python3 programs, export the API key as an env variable:
$ export OPENAI_API_KEY=<your-api-key>
"""

import os
from openai import OpenAI


def embed_loop_text(cl):
    py_loop_text = """
    def what_does_this_do_02(x):
        import math
        if not (isinstance(x, int) and x > 1):
            raise Exception("bad argument")
        if x == 2:
            return (True, 2, "even")
        if x % 2 == 0:
            return (False, 2, "")
        sqrt_x = math.floor(math.sqrt(x))
        for d in range(2, sqrt_x + 1):
            if x % d == 0:
                return (False, d, "")
        return (True, 0, "odd")
    """
    resp = cl.embeddings.create(input=py_loop_text, model="text-embedding-3-small")
    print(resp.data[0].embedding)


if __name__ == "__main__":
    client = OpenAI(
        api_key=os.environ.get(
            "OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"
        )
    )
    embed_loop_text(client)
