"""
https://pypi.org/project/faiss-cpu/

$ python3.11 -m venv ~/teaching/faiss/
$ source ~/teaching/faiss/bin/activate
$ cd ~/teaching/faiss/
$ python3.11 -m pip install --upgrade pip
    pip-25.0.1
$ pip install faiss-cpu
    faiss-cpu-1.10.0 numpy-2.2.4 packaging-24.2
"""

"""
https://github.com/facebookresearch/faiss/wiki/Getting-started
"""

import numpy as np
import faiss


def print_faiss_hnsw_structure(index):
    max_level = index.hnsw.max_level
    ntotal = index.ntotal
    entry_point = index.hnsw.entry_point

    print(f"Max level: {max_level}")
    print(f"Total vectors: {ntotal}")
    print(f"Entry point: {entry_point}, vector: {index.reconstruct(entry_point)}")


def test_hnsw_exp_decay():
    M = 16
    D = 2
    np.random.seed()
    index = faiss.IndexHNSWFlat(D, M)
    node_data = [
        (3, [3.0, 0.0]),
        (8, [8.0, 0.0]),
        (4, [4.0, 0.0]),
        (5, [5.0, 0.0]),
        (11, [11.0, 0.0]),
        (6, [6.0, 1.0]),
        (2, [2.0, 0.0]),
        (7, [7.0, 0.0]),
        (9, [9.0, 0.0]),
        (10, [10.0, 0.0]),
        (12, [12.0, 0.0]),
        (13, [13.0, 0.0]),
        (14, [14.0, 0.0]),
        (1, [1.0, 0.0]),
        (20, [20.0, 0.0]),
        (30, [30.0, 0.0]),
    ]

    vectors = []
    for _, vec in node_data:
        vectors.append(vec)
    x = np.array((vectors)).astype(np.float32)
    index.add(x)
    print(
        f"test_hnsw_exp_decay: max_level {index.hnsw.max_level}, index total {index.ntotal}"
    )
    # print the HNSW structure.
    print_faiss_hnsw_structure(index)
    xq = np.array(([[0.8, 0]])).astype(np.float32)
    D, I = index.search(xq, 4)
    print(D, I)


test_hnsw_exp_decay()


def hnsw_populate_random(n):
    M = 8
    D = 2
    np.random.seed()
    index = faiss.IndexHNSWFlat(D, M)
    population = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index.hnsw.reset()
    max_level = index.hnsw.max_level
    print(f"hnsw_populate_random: max_level {max_level}, index total {index.ntotal}")
    for i in range(n):
        index.add(np.random.random((1, D)).astype(np.float32))
    print(population)
    max_level = index.hnsw.max_level
    print(f"hnsw_populate_random: max_level {max_level}, index total {index.ntotal}")

    entry_point = index.hnsw.entry_point
    print(f"\tLevel {max_level}: 1 element (entry point {entry_point})")
    entry_vector = index.reconstruct(entry_point)
    print(f"\t\tVector: {entry_vector}")


hnsw_populate_random(1024 * 32)


def test_faiss_exp_decay_fn(n):
    M = 16
    D = 2
    np.random.seed()
    index = faiss.IndexHNSWFlat(D, M)
    population = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index.hnsw.reset()
    print(
        f"test_faiss_exp_decay_fn: max_level {index.hnsw.max_level}, index total {index.ntotal}"
    )
    for i in range(n):
        l = index.hnsw.random_level()
        population[l] += 1
    print(population)
    print(
        f"ftest_faiss_exp_decay_fn: max_level {index.hnsw.max_level}, index total {index.ntotal}"
    )


# test_faiss_exp_decay_fn(1024 * 5)

"""
M = 8
>>> hnsw_populate(1000 * 4)
[7143, 915, 121, 12, 0, 1, 0, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 16)
[15003, 948, 45, 4, 0, 0, 0, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 16)
[15003, 948, 45, 4, 0, 0, 0, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 128)
[119842, 7671, 459, 26, 1, 1, 0, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 128)
[119842, 7671, 459, 26, 1, 1, 0, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 512)
[479879, 30149, 1865, 98, 8, 1, 0, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 1024)
[960030, 59972, 3780, 201, 16, 1, 0, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 1024 * 8)
[7679750, 480171, 30050, 1922, 101, 5, 1, 0, 0, 0, 0]
>>> hnsw_populate(1000 * 1024 * 128)
[122880728, 7678938, 480436, 29918, 1859, 112, 8, 1, 0, 0, 0]
"""
