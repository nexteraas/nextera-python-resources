from aa_sequence_map import AaSequenceMap
from sequence_merger import SequenceMerger, AaSequenceMapMerger
from  sanity_checker import SequenceSanityChecker
from features import Features
import evaluation
import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from torch.optim import AdamW
from transformers import (
    RobertaTokenizer, RobertaForSequenceClassification,
    RobertaModel, AutoTokenizer, AutoModelForSequenceClassification,
)

#tokenizer = RobertaTokenizer.from_pretrained("mogam-ai/Ab-RoBERTa", do_lower_case=False)
model_name = "facebook/esm2_t30_150M_UR50D"

tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize_function(example):
    return tokenizer(
        example['sequence'],
        add_special_tokens=True,
        max_length=250,
        padding='max_length',  # True,
        truncation=True,
        return_tensors="pt",
        return_special_tokens_mask=False,
        return_attention_mask=True
)

def _get_model_fn(fold):
    out=f"ab-roberta_fold_{fold}.pt"
    return out

def run_training(train_ds, val_ds, epochs = 3, fold=0):
    train_dataloader = _create_data_loader(train_ds)
    num_labels = 2
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    optimizer = AdamW(model.parameters(), lr=5e-5)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    _run_epochs(device, model, optimizer, train_dataloader, epochs, early_stopping_criteria=3, fold=fold)
    fn=_get_model_fn(fold)
    model.load_state_dict(torch.load(fn, weights_only=True))
    _run_test(device, model, val_ds)

def _run_epochs(device, model, optimizer, train_dataloader, epochs, early_stopping_criteria=3, fold=0):
    best_loss=float('inf')
    early_stopping_counter = 0
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
        if avg_train_loss < best_loss:
            torch.save(model.state_dict(), _get_model_fn(fold))
            best_loss = avg_train_loss
            early_stopping_counter = 0
        else:
            early_stopping_counter += 1
        if early_stopping_counter>=early_stopping_criteria:
            print ('Early stopping triggered')
            break

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


def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    removed = out.remove_sequences(disallowed_aas=['X'])
    if removed > 0:
        print (f"'X'-containing sequences removed from {fn}: {removed}")
    out = out.get_unique_sequences()
    return out

fn1 = "C:/Nextera/div/ab_roberta/mage_vs_prame/chain2_chain1/mage_hs.txt"
fn2 = "C:/Nextera/div/ab_roberta/mage_vs_prame/chain2_chain1/prame_ls.txt"

aa_seq_1 = prepare_input(fn1, 0)
aa_seq_2 = prepare_input(fn2, 1)

checker = SequenceSanityChecker([aa_seq_1, aa_seq_2])
rep=checker.create_std_report()
print(rep)

f=Features()
f.add(aa_seq_1)
f.add(aa_seq_2)
train_f, test_f=f.split_train_test(train_proportion=0.9999999)
balance = None
train_f.iterate_k_fold_validation(run_training, epochs=15,  n_splits=5, shuffle=True, random_state=42, balance=balance)

exit(0)


aa_seq_1 = prepare_input(fn1, 0)
aa_seq_2 = prepare_input(fn2, 1)

# tmp={}
# for s in aa_seq_1.get_sequences():
#     tmp[s]=s
# for s in aa_seq_2.get_sequences():
#     tmp[s]=s
# print (len(tmp))
# print(len(aa_seq_1.get_sequences()) + len(aa_seq_2.get_sequences()))

checker = SequenceSanityChecker([aa_seq_1, aa_seq_2])
rep=checker.create_std_report()
print(rep)

f=Features()
f.add(aa_seq_1)
f.add(aa_seq_2)
train_f, test_f=f.split_train_test(train_proportion=0.9999999)
balance = "max"
train_f.iterate_k_fold_validation(run_training, epochs=15,  n_splits=5, shuffle=True, random_state=42, balance=balance)


# imp_specific = AaSequenceMap(fn1, tag=0)
# imp_specific=imp_specific.get_unique_sequences()
# removed1=imp_specific.remove_sequences(disallowed_aas=['X'])
# imp_background=AaSequenceMap(fn2, tag=1)
# imp_background=imp_background.get_unique_sequences()
# imps = [imp_specific, imp_background]
# checker = SequenceSanityChecker(imps)
# rep=checker.create_std_report()
# print(rep)
#
# f=Features()
# f.add(imp_specific)
# f.add(imp_background)
# f.balance(len(imp_background.get_sequences()))
# train_f, test_f=f.split_train_test(train_proportion=0.9999)
#
# #df=train_f.export_to_dataframe()
#
# train_f.iterate_k_fold_validation(run_training, epochs=15,  n_splits=5, shuffle=True, random_state=42, balance_count=None)
