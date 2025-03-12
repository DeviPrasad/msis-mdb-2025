Transformer Architecture

In a basic transformer architecture, if each token embedding has dimension K 
and the context length is S, then:

The input embedding matrix has shape S × K
Each attention layer processes this S × K matrix
Self-attention operations compute an S × S attention matrix
This requires O(S²) memory and computation complexity

This is why increasing context size has much higher computational cost than 
increasing embedding dimension. The quadratic scaling of attention 
with respect to sequence length (S²) becomes the primary bottleneck
for very long contexts.


Token Embeddings:
Each token in your input text is converted into a high-dimensional vector, 
known as its embedding. For example, if your model has an embedding dimension of 1,024, each token is represented as a 1,024-dimensional vector.

Sequence Input Matrix:
When you have a context size of, say, 2,048 tokens, your model processes 
an input matrix of size 2048×1024 (using our example embedding dimension). 
Each row corresponds to the embedding of a token in the sequence.

Positional Information:
To maintain the order of tokens, positional embeddings (or encodings) are 
added to these token embeddings. This ensures that the model knows the 
position of each token within the context, which is crucial for 
understanding language.

Transformer Attention Mechanism:
The transformer architecture uses these embeddings in its self-attention 
layers, where the model computes relationships between all tokens in the 
context. The context size limits how many tokens can interact in 
these computations.

In summary, the context size determines how many token embeddings 
(augmented with positional information) the model processes at once, and 
these embeddings capture the semantic and syntactic features of the tokens.