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
    M = 16
    D = 2
    np.random.seed()
    index = faiss.IndexHNSWFlat(D, M)
    population = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index.hnsw.reset()
    for i in range(n):
        l = index.hnsw.random_level()
        population[l] += 1
        index.add(np.random.random((1, D)).astype(np.float32))
    print(population)


hnsw_populate(1000)
