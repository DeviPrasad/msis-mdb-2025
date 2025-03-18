##
## tensorflow
## https://www.tensorflow.org/install/pip#macos
## Note: Requires Python 3.9–3.11, and pip >= 20.3 for MacOS.
## $ pip install torch
##   mpmath-1.3.0 sympy-1.13.3 torch-2.2.2
## $ python3.11 -m pip install transformers[tf-cpu]


import torch
import numpy as np
from transformers import BertModel
from transformers import BertTokenizer


words_1 = """
    university computer programming engineering systems development researchers AI ML neural algebra
"""
words_2 = "professors  software algorithm science software algorithms learning data vector machine  math"


def test_cs_edu(tokenizer, model):
    token_set_1 = tokenizer.tokenize(words_1)
    token_set_1_ids = tokenizer.convert_tokens_to_ids(token_set_1)
    assert len(token_set_1) == len(token_set_1_ids)
    print(token_set_1)

    embedding_1 = model.embeddings.word_embeddings(torch.tensor(token_set_1_ids))
    assert embedding_1.shape == torch.Size([len(token_set_1), 768])

    token_set_2 = tokenizer.tokenize(words_2)
    token_set_2_ids = tokenizer.convert_tokens_to_ids(token_set_2)
    assert len(token_set_2) == len(token_set_2_ids)
    print(token_set_2)

    embedding_2 = model.embeddings.word_embeddings(torch.tensor(token_set_2_ids))
    assert embedding_2.shape == torch.Size([len(token_set_2), 768])

    cos = torch.nn.CosineSimilarity(dim=1)
    similarity = cos(embedding_1, embedding_2)
    print("similarity via bert model")
    for i in range(len(token_set_1)):
        print(f"{i:>5}  {token_set_1[i]:<16} {token_set_2[i]:<16} {similarity[i]}")


def test_bert_embeddings():
    ## https://huggingface.co/transformers/v3.0.2/model_doc/bert.html
    ## model size - 440M bytes
    bert_model = BertModel.from_pretrained(
        "bert-base-uncased", torch_dtype=torch.float16, attn_implementation="sdpa"
    )
    bert_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    test_cs_edu(bert_tokenizer, bert_model)


if __name__ == "__main__":
    test_bert_embeddings()
