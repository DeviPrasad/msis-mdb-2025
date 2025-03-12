# Faiss
https://github.com/facebookresearch/faiss

### Faiss wiki
https://github.com/facebookresearch/faiss/wiki

# FB Engineering Blog
https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/


import numpy as np
import time

def dot_product(a, b):
    return np.dot(a, b)

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

def calc():
    # Large vector for comparison
    n = 1_000_000
    vector1 = np.random.rand(n)
    vector2 = np.random.rand(n)
    # Time dot product
    start = time.time()
    dot_result = dot_product(vector1, vector2)
    dot_time = time.time() - start
    # Time Euclidean distance
    start = time.time()
    distance_result = euclidean_distance(vector1, vector2)
    distance_time = time.time() - start
    print(f"Dot Product Time: {dot_time:.6f} seconds")
    print(f"Euclidean Distance Time: {distance_time:.6f} seconds")
    print(f"Dot Product is {distance_time/dot_time:.2f}x faster")
