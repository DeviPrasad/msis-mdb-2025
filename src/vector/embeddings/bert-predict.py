import torch
from transformers import BertTokenizer, BertModel, BertForMaskedLM
import logging

logging.basicConfig(level=logging.WARN)  # OPTIONAL
logging.disable(logging.WARNING)

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForMaskedLM.from_pretrained("bert-base-uncased")
model.eval()
# model.to('cuda') # if have gpu


def predict_masked_sent(text, top_k=5):
    # Tokenize input
    text = "[CLS] %s [SEP]" % text
    tokenized_text = tokenizer.tokenize(text)
    masked_index = tokenized_text.index("[MASK]")
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    # tokens_tensor = tokens_tensor.to('cuda')    # if have gpu

    # Predict all tokens
    outputs = model(tokens_tensor)
    predictions = outputs[0]

    probs = torch.nn.functional.softmax(predictions[0, masked_index], dim=-1)
    top_k_weights, top_k_indices = torch.topk(probs, top_k, sorted=True)
    return (masked_index, top_k_weights, top_k_indices)


def display_predictions(text, mask_pos, top_k_weights, top_k_indices):
    print()
    print(f"Masked word at {mask_pos}; prediction for '{text}'")
    for i, pred_idx in enumerate(top_k_indices):
        predicted_token = tokenizer.convert_ids_to_tokens([pred_idx])[0]
        token_weight = top_k_weights[i]
        print(f"{predicted_token:<16} {token_weight:>10}")


if __name__ == "__main__":
    masked_index, weights, indices = predict_masked_sent(
        "Android is a [MASK] operating system", top_k=4
    )
    display_predictions(
        "Android is a [MASK] operating system", masked_index, weights, indices
    )

    masked_index, weights, indices = predict_masked_sent(
        "[MASK] is the company that owns iPhones", top_k=4
    )
    display_predictions(
        "[MASK] is the company that makes iPhones", masked_index, weights, indices
    )
