import os
from openai import OpenAI
import numpy as np


def embed_loop_text(cl):
    py_loop_text = """
    # python code to determine if 'x' is a prime number.
    def is_prime(x):
        import math
        if not (isinstance(x, int) and x > 1):
            raise Exception("bad argument")
        if x == 2:
            # 2 is an even prime
            return (True, 2, "even")
        if x % 2 == 0:
            return (False, 2, "")
        sqrt_x = math.floor(math.sqrt(x))
        # main loop
        for d in range(2, sqrt_x + 1):
            if x % d == 0:
                return (False, d, "")
        return (True, 0, "odd")
    """
    resp = cl.embeddings.create(input=py_loop_text, model="text-embedding-3-small")
    # print(resp.data[0].embedding)
    return resp.data[0].embedding


def embed_text(cl, text):
    resp = cl.embeddings.create(input=text, model="text-embedding-3-small")
    return (resp, resp.data[0].embedding)


def embed_query_prime_number(cl):
    feature_query_prime_number = "python code for testing prime numbers"
    resp = cl.embeddings.create(
        input=feature_query_prime_number, model="text-embedding-3-small"
    )
    return resp.data[0].embedding


def cosine_similarity(v1, v2):
    l1 = np.linalg.norm(v1)
    l2 = np.linalg.norm(v2)
    if l1 == 0 or l2 == 0:
        raise ZeroDivisionError()
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def test_cs_edu(cl):
    _, edu_embedding = embed_text(
        cl,
        "university computer-science undergraduate-degree programming engineering systems-development professors researchers programmers AI ML neural networks linear algebra",
    )
    edu_vec = np.array(edu_embedding)
    sub_names = "distributed-systems programming software algorithms data structures machine learning operating-systems vector-databases OpenAI "
    sub_embed_resp, sub_embedding = embed_text(
        cl,
        sub_names,
    )
    alg_vec = np.array(sub_embedding)
    print(f"cs-education: {cosine_similarity(edu_vec, alg_vec)}")  # 0.6441489438955207
    # print(sub_embed_resp)

    import tiktoken

    enc = tiktoken.get_encoding("cl100k_base")
    token_ids = enc.encode(sub_names)
    print(token_ids)
    print([enc.decode_single_token_bytes(token_id) for token_id in token_ids])


def check_similarity(cl):
    py_code_embedding = embed_loop_text(cl)
    _, loop_embedding = embed_text(cl, "code executing a loop")
    prime_num_embedding = embed_query_prime_number(cl)
    _, iteration_embedding = embed_text(cl, "iteration")

    py_code_vec = np.array(py_code_embedding)
    loop_vec = np.array(loop_embedding)
    prime_number_query_vec = np.array(prime_num_embedding)
    iteration_vec = np.array(iteration_embedding)

    cos_code_prime_num = cosine_similarity(py_code_vec, prime_number_query_vec)
    cos_code_loop = cosine_similarity(py_code_vec, loop_vec)
    cos_loop_prime_num = cosine_similarity(loop_vec, prime_number_query_vec)
    cos_loop_iteration = cosine_similarity(iteration_vec, loop_vec)

    print(
        f"code-loop {cos_code_loop}, code-prime {cos_code_prime_num}, loop-prime {cos_loop_prime_num}, loop-iteration {cos_loop_iteration}"
    )

    print(f"self-similar: {cosine_similarity(loop_vec, loop_vec)}")


def test_openai_embeddings():
    client = OpenAI(
        api_key=os.environ.get(
            "OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"
        )
    )
    test_cs_edu(client)
    check_similarity(client)


def test_cosine_similarity():
    # reason?
    assert cosine_similarity(np.array([1, 0]), np.array([0, 1])) == 0
    assert cosine_similarity(np.array([4, 4]), np.array([27.8679, -27.8679])) == 0
    assert cosine_similarity(np.array([27.32, 0]), np.array([0, -11.8156])) == 0
    assert cosine_similarity(np.array([-5, 0]), np.array([0, -3])) == 0
    # reason?
    assert cosine_similarity(np.array([1, 2, 3]), np.array([-7, -14, -21])) == -1
    assert np.isclose(
        cosine_similarity(np.array([7, 7]), np.array([-4, -4])), -1.0, rtol=1e-04
    )
    try:
        cosine_similarity(np.array([0, 0, 0]), np.array([-7, -14, -21]))
    except ZeroDivisionError as zde:
        pass

    # reason?
    assert cosine_similarity(np.array([1, 1]), np.array([3, 3])) == 1

    # what happens if rtol=1e-04?
    assert np.isclose(
        cosine_similarity(np.array([3, 3]), np.array([2.99, 2.78])), 1, rtol=1e-03
    )


def test_vector_product():
    assert np.dot([0.2, 0.7, 0.8, 0.7], [0.5, 0.5, 0.5, 0.5]) == (
        0.1 + 0.35 + 0.4 + 0.35
    )
    assert np.dot(
        [0.892, -0.3657, 0.9888, 0.72139244], [0.126, 0.462, 0.03, 0.99]
    ) == np.float64(0.6872811156)


if __name__ == "__main__":
    test_openai_embeddings()
    test_vector_product()
    test_cosine_similarity()
