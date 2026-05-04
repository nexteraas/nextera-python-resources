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


dataset=f.export_to_dataset(randomize=True)





model_checkpoint = "facebook/esm2_t30_150M_UR50D"


from sklearn.model_selection import StratifiedKFold
import numpy as np

metric = load("accuracy")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return metric.compute(predictions=predictions, references=labels)


# Assuming 'dataset' is a Hugging Face Dataset object
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
labels = dataset['label']  # Extract labels for stratification

results = []

for fold, (train_idx, val_idx) in enumerate(skf.split(np.zeros(len(labels)), labels)):
    print(f"--- Training Fold {fold + 1} ---")

    # Create fold-specific datasets
    train_fold = dataset.select(train_idx)
    val_fold = dataset.select(val_idx)

    # Initialize a NEW model for each fold to avoid data leakage
    model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=2)

    batch_size = 8

    # Update training arguments for each fold (e.g., unique output directory)
    training_args = TrainingArguments(
        output_dir=f"./results_fold_{fold}",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        push_to_hub=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_fold,
        eval_dataset=val_fold,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    fold_metrics = trainer.evaluate()
    results.append(fold_metrics)

# Calculate final average across all folds
avg_accuracy = np.mean([res['eval_accuracy'] for res in results])
print(f"Average Cross-Validation Accuracy: {avg_accuracy}")



exit(0)




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




def run_fold():
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

    train_tokenized = tokenizer(train_sequences)
    test_tokenized = tokenizer(test_sequences)

    train_dataset = Dataset.from_dict(train_tokenized)
    test_dataset = Dataset.from_dict(test_tokenized)

    train_dataset = train_dataset.add_column("labels", train_labels)
    test_dataset = test_dataset.add_column("labels", test_labels)

    num_labels = max(train_labels + test_labels) + 1  # Add 1 since 0 can be a label
    model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=num_labels)

    model_name = model_checkpoint.split("/")[-1]
    batch_size = 8

    args = TrainingArguments(
        f"{model_name}-finetuned-localization",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        push_to_hub=False,
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


train_sequences, test_sequences, train_labels, test_labels = train_test_split(sequences, labels, test_size=0.25, shuffle=True)



