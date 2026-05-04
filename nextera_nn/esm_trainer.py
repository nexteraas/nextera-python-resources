from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from evaluate import load
import numpy as np
from aa_sequence_map import AaSequenceMap
from sequence_merger import SequenceMerger, AaSequenceMapMerger
from  sanity_checker import SequenceSanityChecker
from features import Features


model_checkpoint = "facebook/esm2_t12_35M_UR50D"















def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    removed = out.remove_sequences(disallowed_text=['X','MISSING'])
    out = out.get_unique_sequences()
    return out

fn1 = "C:/Nextera/div/ab_roberta/mage_vs_prame/chain2_chain1/mage_hs_2.txt"
fn2 = "C:/Nextera/div/ab_roberta/mage_vs_prame/chain2_chain1/prame_hs_2.txt"

aa_seq_1 = prepare_input(fn1, 0)
aa_seq_2 = prepare_input(fn2, 1)

checker = SequenceSanityChecker([aa_seq_1, aa_seq_2])
rep=checker.create_std_report()
print(rep)

f=Features()
f.add(aa_seq_1)
f.add(aa_seq_2)


df=f.export_to_dataframe(randomize=True)
sequences = df['sequence'].tolist()
labels = df['label'].tolist()





train_sequences, test_sequences, train_labels, test_labels = train_test_split(sequences, labels, test_size=0.25, shuffle=True)



tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

train_tokenized = tokenizer(train_sequences)
test_tokenized = tokenizer(test_sequences)

train_dataset = Dataset.from_dict(train_tokenized)
test_dataset = Dataset.from_dict(test_tokenized)

train_dataset

train_dataset = train_dataset.add_column("labels", train_labels)
test_dataset = test_dataset.add_column("labels", test_labels)


num_labels = max(train_labels + test_labels) + 1  # Add 1 since 0 can be a label
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=num_labels)

model_name = model_checkpoint.split("/")[-1]
batch_size = 8

args = TrainingArguments(
    f"{model_name}-finetuned-localization",
    eval_strategy = "epoch",
    save_strategy = "epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=3,
    weight_decay=0.01,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    push_to_hub=True,
)

metric = load("accuracy")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return metric.compute(predictions=predictions, references=labels)

trainer = Trainer(
    model,
    args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()