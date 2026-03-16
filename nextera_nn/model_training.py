from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
from features import Features
import evaluation
import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from torch.optim import AdamW
from transformers import (
    RobertaTokenizer,
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
    optimizer = AdamW(model.parameters(), lr=5e-5)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    first_model, best_model = _run_epochs(device, model, optimizer, train_dataloader, epochs)
    #_run_test(device, model, val_ds)
    print('First model:')
    _run_test(device, first_model, val_ds)
    print('Best model:')
    _run_test(device, best_model, val_ds)

def _run_epochs(device, model, optimizer, train_dataloader, epochs):
    first_model = None
    best_model = None
    best_loss=float('inf')
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
        if avg_train_loss < best_loss:
            best_loss = avg_train_loss
            best_model = model
        if first_model is None:
            first_model = model
        print(f"Epoch {epoch + 1}, Average Training Loss: {avg_train_loss:.4f}")
    return first_model, best_model

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


imp_specific = AaSequenceMap("C:/Nextera/div/ab_roberta/mage_vs_prame/tbl_R3-MAGE_2.txt", tag=0)
imp_specific=imp_specific.get_unique_sequences()
#imp_specific=FastaImporter("C:/Nextera/div/ab_roberta/test.fa", True, True)
removed1=imp_specific.remove_sequences(disallowed_aas=['X'])
imp_background=AaSequenceMap("C:/Nextera/div/ab_roberta/mage_vs_prame/tbl_R3-PRAME_2.txt", tag=1)
imp_background=imp_background.get_unique_sequences()
imps = [imp_specific, imp_background]
checker = SequenceSanityChecker(imps)
rep=checker.create_std_report()
print(rep)

f=Features()
f.add(imp_specific)
f.add(imp_background)
f.balance()
train_f, test_f=f.split_train_test(train_proportion=0.99)

df=train_f.export_to_dataframe()

train_f.iterate_k_fold_validation(run_training, epochs=20,  n_splits=5, shuffle=True, random_state=42)
