##
## tensorflow
## https://www.tensorflow.org/install/pip#macos
## Note: Requires Python 3.9–3.11, and pip >= 20.3 for MacOS.
## $ python3.11 -m venv ~/teaching/tfvec
##
## $ source ~/teaching/tfvec/bin/activate
## $ cd  ~/teaching/tfvec
## $ python3.11 -m pip install --upgrade pip
## $ python3 --version == Python 3.11.11
## $ python3 -m pip --version == pip 25.0.1 from ~/teaching/tfvec/lib/python3.11/site-packages/pip (python 3.11)
## $ pip install sentence_transformers
## $ python3.11 -m pip install transformers[tf-cpu]
## -- Installing huggingface-hub-0.29.1 kagglehub-0.3.10 keras-2.15.0 keras-core-0.1.7 keras-nlp-0.12.1
## -- safetensors-0.5.3 tensorboard-2.15.2 tensorflow-2.15.1 tensorflow-cpu-2.15.1
## -- tensorflow-estimator-2.15.0 tensorflow-hub-0.16.1 tensorflow-probability-0.23.0
## -- tensorflow-text-2.15.0 tf-keras-2.15.1 tokenizers-0.21.0 tqdm-4.67.1 transformers-4.49.0
## $ pip install tensorflow
## -- Installing collected packages: tensorflow-io-gcs-filesystem, numpy, google-pasta, keras, tensorflow
## -- Successfully installed MarkupSafe-3.0.2 absl-py-2.1.0 astunparse-1.6.3 certifi-2025.1.31
## -- keras-3.9.0 numpy-1.26.4 tensorflow-2.16.2
## $ pip install tensorflow-datasets
## $ pip install accelerate

## $ pip install psycopg2
## $ pip install pgvector

## https://sbert.net/index.html
"""
Computing Embeddings
"""
## https://sbert.net/examples/applications/computing-embeddings/README.html#calculating-embeddings
from sentence_transformers import SentenceTransformer

st_ex_sentence = "This is an example sentence used for demonstration in BDA-2025 class!"
st_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
st_embedding = st_model.encode(st_ex_sentence)
assert st_embedding.shape == (384,)
print(st_embedding)

#####

#####
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
###

import torch
from transformers import BertModel
from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
king_token_id = tokenizer.convert_tokens_to_ids(["king"])[0]
king_embedding = model.embeddings.word_embeddings(torch.tensor([king_token_id]))
queen_token_id = tokenizer.convert_tokens_to_ids(["queen"])[0]
queen_embedding = model.embeddings.word_embeddings(torch.tensor([queen_token_id]))
cos = torch.nn.CosineSimilarity(dim=1)
similarity = cos(king_embedding, queen_embedding)
print(similarity[0])
# >> tensor(0.6469, grad_fn=<SelectBackward0>)
man_token_id = tokenizer.convert_tokens_to_ids(["man"])[0]
man_embedding = model.embeddings.word_embeddings(torch.tensor([man_token_id]))
similarity = cos(king_embedding, man_embedding)
print(similarity[0])
# >> tensor(0.3533, grad_fn=<SelectBackward0>)

###

from transformers import AutoTokenizer
from transformers import AutoConfig, TFAutoModel

model = TFAutoModel.from_pretrained("google-bert/bert-base-cased")
tokenizer = AutoTokenizer.from_pretrained(model, token="HF_TOKEN")


## https://www.tensorflow.org/text/guide/word_embeddings
import io
import os
import re
import shutil
import string
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.layers import TextVectorization

url = "https://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"
dataset = tf.keras.utils.get_file(
    "aclImdb_v1.tar.gz", url, untar=True, cache_dir=".", cache_subdir=""
)
dataset_dir = os.path.join(os.path.dirname(dataset), "aclImdb")
os.listdir(dataset_dir)
# ["imdbEr.txt", "test", "imdb.vocab", "README", "train"]
train_dir = os.path.join(dataset_dir, "train")
os.listdir(train_dir)
# ['urls_unsup.txt', 'neg', 'urls_pos.txt', 'unsup', 'urls_neg.txt', 'pos', 'unsupBow.feat', 'labeledBow.feat']
remove_dir = os.path.join(train_dir, "unsup")
shutil.rmtree(remove_dir)

batch_size = 1024
seed = 123
train_ds = tf.keras.utils.text_dataset_from_directory(
    "aclImdb/train",
    batch_size=batch_size,
    validation_split=0.2,
    subset="training",
    seed=seed,
)
val_ds = tf.keras.utils.text_dataset_from_directory(
    "aclImdb/train",
    batch_size=batch_size,
    validation_split=0.2,
    subset="validation",
    seed=seed,
)
#
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


##-----
# import transformers
# from transformers import BertModel
# from transformers import BertTokenizer
