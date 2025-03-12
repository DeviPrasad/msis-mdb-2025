# Motivation for Vector Databases

In AI multi-modal data needs to be represented in an uniform manner.
ML algorithms and various model architectures process vector data.

Solutions that need a bit of AI enhancement integrate with databases specializing in vector data.

```
Data  --> Deep Learning ML Models --> Vector Embedding --> |Vector DB|
```
Note that *vector embeddings* are *learned* outputs of ML Models.

```
Query --> Deep Learning ML Models --> Vector Embedding --> Nearest Neighbor Search Algorithm --> |Vector DB|
```

It is more common to refer to embeddings when talking about dense vectors learned using neural networks.

Embeddings are specifically referred to a representation of data in some space. This in general means the internal way an ML model (neural network, LLM network, etc...) represents data.

Often these are used *externally* as well, but they have little semantic meaning.



```python

"""
Computing Embeddings with SentenceTransformer
"""
## https://sbert.net/index.html
## https://sbert.net/examples/applications/computing-embeddings/README.html#calculating-embeddings
from sentence_transformers import SentenceTransformer

st_ex_sentence = "This is an example sentence used for demonstration in BDA-2025 class!"
st_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
st_embedding = st_model.encode(st_ex_sentence)
assert st_embedding.shape == (384,)
print(st_embedding)

```

```python

import torch
from transformers import BertModel
from transformers import BertTokenizer

ex_sentence = "This is an example sentence used for demonstrating how to compute vector embedding with BERT pre-trained model, in BDA-2025 class!"

## https://huggingface.co/transformers/v3.0.2/model_doc/bert.html
## model size - 440M bytes
bert_model = BertModel.from_pretrained("bert-base-uncased")
bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

bert_tokens = bert_tokenizer.tokenize(ex_sentence)
bert_token_ids = bert_tokenizer.convert_tokens_to_ids(bert_tokens)
assert len(bert_tokens) == len(bert_token_ids)
bert_embedding = bert_model.embeddings.word_embeddings(torch.tensor(bert_token_ids))
assert bert_embedding.shape == torch.Size([len(bert_tokens), 768])

```

## Popular Vector Embedding APIs
- [OpenAI] (https://platform.openai.com/docs/overview)

- []

- [Cohere]


- PostgreSQL version 9 has a vector extension with which it supports vector data type.




## Specialized PRoducts

Qdrant https://qdrant.tech/documentation/overview/

Marqo https://docs.marqo.ai/latest/reference/api/indexes/create-structured-index/


# Vector Databases

Recent applications
- multi-modal search
- similarity search
- recommendation engines
- LLMs


### Use cases
- analytical and generative AI
    - natural language processing
    - production-level LLM caching
        - low latency
        - high scalability, and
        - high availability.
    - video and image recognition
    - recommendation system
    - search
    - identify patterns dissimilar from predominant patterns
        - data anomalies
        - fraudulent activities
- identify similar
    - images, documents, and songs based on their contents, themes, sentiments, and styles
    - products based on their characteristics, features, and user groups
- recommend contents, products, or services based on individuals' preferences
- implement persistent memory for AI agents


## Vector DB
Designed to store and manage vector embeddings
- representations of data in a high-dimensional space
- each dimension corresponds to a feature of the data
- tens of thousands of dimensions are generally  used
- vector's position in this space represents its characteristics

Embeddings are indexed and queried through vector search algorithms based on their vector distance or similarity.


## Embeddings
The idea of vector semantics is to represent a word as a point in a multidimensional semantic space that is derived from the distributions of word neighbors.

Vectors for representing words are called embeddings. The word “embedding” derives from its mathematical sense as a mapping from one space or structure to another.

https://platform.openai.com/docs/guides/embeddings#what-are-embeddings
- An embedding is a vector (list) of floating point numbers.
- The distance between two vectors measures their relatedness.
- Small distances suggest high relatedness and large distances suggest low relatedness.

The embedding is an information dense representation of the semantic meaning of a piece of text. Each embedding is a vector of floating-point numbers, such that the distance between two embeddings in the vector space is correlated with semantic similarity between two inputs in the original format. For example, if two texts are similar, then their vector representations should also be similar.


### Token Embeddings
- Each token in our input text is converted into a high-dimensional vector, known as its embedding
- If our model has an embedding dimension of 1,024, each token is represented as a 1,024-dimensional vector.

Each token’s embedding is a high-dimensional vector. This allows the model to capture a wide range of linguistic features and nuances, like the meaning of a word, its part of speech, and its relationship to other words in the sentence.

## Vector Databases - Basics
https://book.premai.io/state-of-open-source-ai/vector-db/

## vector search algorithms
- Exhaustive K-nearest neighbors (KNN)
- Approximate Nearest Neighbor (ANN)
- Hierarchical Navigable Small World (HNSW)
-

Microsoft CosmosBD supports
 - k-nearest neighbors (kNN)
 - Approximate nearest neighbor (ANN)


Vector Indexing Algorithms
- quickly find vectors with an acceptable accuracy
- Approximate Nearest Neighbor (ANN) algorithms
    - Hierarchical Navigable Small World (HNSW) graphs
        - scales logarithmically even in high-dimensional data
        - https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world
    - KD-trees
    - Inverted File (IVF)
        - https://zilliz.com/learn/how-to-pick-a-vector-index-in-milvus-visual-guide#Inverted-File-FLAT-IVF-FLAT-Index

    - Inverted File Index with Quantization (IVF-SQ8 and IVF-PQ)
        - https://zilliz.com/learn/how-to-pick-a-vector-index-in-milvus-visual-guide#Inverted-File-Index-with-Quantization-IVF-SQ8-and-IVF-PQ
