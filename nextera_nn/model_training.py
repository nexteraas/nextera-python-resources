from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
from features import Features
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
    #tokenizer = RobertaTokenizer.from_pretrained("mogam-ai/Ab-RoBERTa", do_lower_case=False)
    # applying the tokenization function to the entire dataset in batches
    tokenized_dataset = train_ds.map(tokenize_function, batched=True)
    df_train = tokenized_dataset.to_pandas()
    # extracting input_ids, attention mask, and label from the DataFrame and converting to numpy array
    X_train_inputs = np.array(list(df_train['input_ids']))
    X_train_attention = np.array(list(df_train['attention_mask']))
    y_train = df_train['label']
    # converting to tensors
    train_inputs = torch.tensor(X_train_inputs)
    train_attention = torch.tensor(X_train_attention)
    train_labels = torch.tensor(y_train.values)
    # creating a TensorDataset from inputs, attention masks, and labels
    train_data = TensorDataset(train_inputs, train_attention, train_labels)
    # creating a DataLoader for batching the train data
    train_dataloader = DataLoader(train_data, batch_size=16, shuffle=True)
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

def _run_test(test_ds):
    tokenized_dataset = test_ds.map(tokenize_function, batched=True)
    df_test = tokenized_dataset.to_pandas()
    X_test_inputs = np.array(list(df_test['input_ids']))
    X_test_attention = np.array(list(df_test['attention_mask']))
    y_test = df_test['signal']
    # converting input_ids to tensor
    test_inputs = torch.tensor(X_test_inputs)
    test_attention = torch.tensor(X_test_attention)
    test_labels = torch.tensor(y_test.values)
    # creating a TensorDataset & DataLoader from inputs, attention masks, and labels
    test_data = TensorDataset(test_inputs, test_attention, test_labels)
    test_dataloader = DataLoader(test_data, batch_size=16)

def get_predictions(device, model, dataloader):
    # setting the model to evaluation mode
    model.eval()
    predictions = []
    true_labels = []
    with torch.no_grad():
        for batch in dataloader:
            b_input_ids, b_attention_mask, b_labels = [t.to(device) for t in batch]
            # forward pass to obtain model outputs
            outputs = model(b_input_ids, attention_mask=b_attention_mask)
            # extracting logits
            logits = outputs.logits
            # predicting the class with the highest score
            predicted_class = torch.argmax(logits, dim=1)
            # storing predictions and true labels for the current batch
            predictions.extend(predicted_class.cpu().numpy())
            true_labels.extend(b_labels.cpu().numpy())
    return predictions, true_labels






imp_specific = AaSequenceMap("C:/Nextera/div/ab_roberta/prame_specific_seqs.txt", tag=0)
#imp_specific=FastaImporter("C:/Nextera/div/ab_roberta/test.fa", True, True)
removed1=imp_specific.remove_sequences(disallowed_aas=['X'])
imp_background=AaSequenceMap("C:/Nextera/div/ab_roberta/r0_n_250.txt", tag=1)
imps=[imp_specific, imp_background]
checker= SequenceSanityChecker(imps)
checker.check_aas()
max1=checker.get_max_lengths(imp_specific)
max2=checker.get_max_lengths(imp_background)
aacount1=checker.check_unique_aa_counts(position_from=-2, position_to=None, aa_sequence_map=imp_specific)
aacount2=checker.check_unique_aa_counts(position_from=-2, position_to=None, aa_sequence_map=imp_background)

single_occ_CAR=checker.check_motif('CAR')
multi_occ_CAR=checker.check_motif('CAR', multiple_occurrences_only=True)

single_occ_WG=checker.check_motif('WG')
multi_occ_WG=checker.check_motif('WG', multiple_occurrences_only=True)

single_occ_TVSS=checker.check_motif('TVSS')
multi_occ_TVSS=checker.check_motif('TVSS', multiple_occurrences_only=True)


f=Features()
f.add(imp_specific)
f.add(imp_background)
f.balance()
train_f, test_f=f.split_train_test()

df=train_f.export_to_dataframe()

train_f.iterate_k_fold_validation(run_training, n_splits=5, shuffle=True, random_state=42)

df=9