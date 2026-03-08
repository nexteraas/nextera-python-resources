from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
from features import Features
import evaluation
from datasets import Dataset
import torch
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
from torch.optim import AdamW
from transformers import (
    RobertaTokenizer,
    RobertaModel,
    RobertaForMaskedLM,
    RobertaForSequenceClassification,
)

tokenizer = RobertaTokenizer.from_pretrained("mogam-ai/Ab-RoBERTa", do_lower_case=False)

def tokenize_function(example):
    return tokenizer(
        example['sequence'],
        add_special_tokens=True,
        max_length=150,
        padding='max_length',  # True,
        truncation=True,
        return_tensors="pt",
        return_special_tokens_mask=False,
        return_attention_mask=True
)

def run_training(train_ds, val_ds, epochs = 3):
    train_dataloader = _create_data_loader(train_ds)
    model_name = "mogam-ai/Ab-RoBERTa"
    num_labels = 2
    # model = RobertaModel.from_pretrained(model_name, add_pooling_layer=False)
    model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    # set up the optimizer
    optimizer = AdamW(model.parameters(), lr=5e-5)
    # put the model on device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    _run_epochs(device, model, optimizer, train_dataloader, epochs)
    _run_test(device, model, val_ds)

def _run_epochs(device, model, optimizer, train_dataloader, epochs):
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_dataloader:
            b_input_ids, b_attention_mask, b_labels = [t.to(device) for t in batch]
            model.zero_grad()
            outputs = model(b_input_ids, attention_mask=b_attention_mask, labels=b_labels)
            loss = outputs.loss
            total_loss += loss.item()
            loss.backward()
            optimizer.step()
        avg_train_loss = total_loss / len(train_dataloader)
        print(f"Epoch {epoch + 1}, Average Training Loss: {avg_train_loss:.4f}")

def _run_test(device, model, test_ds):
    test_dataloader = _create_data_loader(test_ds)
    baseline_predictions, true_labels = evaluation._get_predictions(device, model, test_dataloader)
    evaluation._print_report(true_labels, baseline_predictions)

def _create_data_loader(ds):
    tokenized_dataset = ds.map(tokenize_function, batched=True)
    df = tokenized_dataset.to_pandas()
    X_inputs = np.array(list(df['input_ids']))
    X_attention = np.array(list(df['attention_mask']))
    y = df['label']
    inputs = torch.tensor(X_inputs)
    attention = torch.tensor(X_attention)
    labels = torch.tensor(y.values)
    t_ds = TensorDataset(inputs, attention, labels)
    out = DataLoader(t_ds, batch_size=16, shuffle=True)
    return out


imp_specific = AaSequenceMap("C:/Nextera/div/ab_roberta/prame_specific_seqs.txt", tag=0)
#imp_specific=FastaImporter("C:/Nextera/div/ab_roberta/test.fa", True, True)
removed1=imp_specific.remove_sequences(disallowed_aas=['X'])
imp_background=AaSequenceMap("C:/Nextera/div/ab_roberta/EXPLORER/r0_n250_ighv.txt", tag=1)
imps=[imp_specific, imp_background]
checker= SequenceSanityChecker(imps)
rep=checker.create_std_report()
print(rep)

f=Features()
f.add(imp_specific)
f.add(imp_background)
f.balance()
train_f, test_f=f.split_train_test(train_proportion=0.99)

df=train_f.export_to_dataframe()

train_f.iterate_k_fold_validation(run_training, n_splits=5, shuffle=True, random_state=42)

df=9