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


def hnsw_populate(n):
    M = 8
    D = 2
    np.random.seed()
    index = faiss.IndexHNSWFlat(D, M)
    population = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index.hnsw.reset()
    print(f"max_level {index.hnsw.max_level}, index total {index.ntotal}")
    for i in range(n):
        l = index.hnsw.random_level()
        population[l] += 1
        index.add(np.random.random((1, D)).astype(np.float32))
    print(population)
    print(f"max_level {index.hnsw.max_level}, index total {index.ntotal}")


hnsw_populate(1024 * 8)

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
