from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from evaluate import load
from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
from features import Features
from sklearn.model_selection import StratifiedKFold
import numpy as np


class EsmTrainer():
    def __init__(self, model, dataset, skf, batch_size=8):
        self._skf = skf
        self._model = model
        self._batch_size = batch_size
        self._dataset = dataset.map(self._tokenize_function, batched=True)
        self._labels = self._dataset['label']
        self._metric = load("accuracy")

    def _tokenize_function(self, example):
        tokenizer = AutoTokenizer.from_pretrained(self._model)
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

    def _compute_metrics(self, eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return self._metric.compute(predictions=predictions, references=labels)

    def _run_fold(self, train_idx, val_idx, fold, results):
        train_fold = self._dataset.select(train_idx)
        val_fold = self._dataset.select(val_idx)
        model = AutoModelForSequenceClassification.from_pretrained(self._model, num_labels=2)
        training_args = TrainingArguments(
            output_dir=f"./results_fold_{fold}",
            eval_strategy="epoch", save_strategy="epoch", learning_rate=2e-5,
            per_device_train_batch_size=self._batch_size, per_device_eval_batch_size=self._batch_size,
            num_train_epochs=3, weight_decay=0.01,
            load_best_model_at_end=True, metric_for_best_model="accuracy", push_to_hub=False,
        )
        trainer = Trainer(model=model, args=training_args,
                          train_dataset=train_fold, eval_dataset=val_fold, compute_metrics=self._compute_metrics, )
        trainer.train()
        fold_metrics = trainer.evaluate()
        results.append(fold_metrics)

    def train(self):
        results = []
        for fold, (train_idx, val_idx) in enumerate(self._skf.split(np.zeros(len(self._labels)), self._labels)):
            self._run_fold(train_idx, val_idx, fold,  results=results)
        avg_accuracy = np.mean([res['eval_accuracy'] for res in results])
        print(f"Average Cross-Validation Accuracy: {avg_accuracy}")




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


skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
esmt=EsmTrainer(model="facebook/esm2_t30_150M_UR50D", dataset=f.export_to_dataset(), skf=skf, batch_size=8)
esmt.train()