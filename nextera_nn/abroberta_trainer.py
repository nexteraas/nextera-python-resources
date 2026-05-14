from transformers import AutoTokenizer, EarlyStoppingCallback
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer, RobertaForSequenceClassification
from evaluate import load
from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
from features import Features
from sklearn.model_selection import StratifiedKFold
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support


class AbRobertaTrainer():
    def __init__(self, model, dataset, skf, epochs=3, batch_size=8, metric_for_best_model="accuracy" ):
        self._skf = skf
        self._model = model
        self._batch_size = batch_size
        self._dataset = dataset.map(self._tokenize_function, batched=True)
        self._labels = self._dataset['label']
        self._metric = load("accuracy")
        self._epochs = epochs
        if metric_for_best_model!='accuracy' and metric_for_best_model!='eval_loss':
            raise ValueError("Only 'accuracy' or 'eval_loss' are supported.")
        self._metric_for_best_model = metric_for_best_model
        self._cache_eval_pred = None


    def _tokenize_function(self, example):
        tokenizer = AutoTokenizer.from_pretrained(self._model)
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

    def _compute_metrics(self, eval_pred):
        self._cache_eval_pred = eval_pred
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        #print(classification_report(labels, predictions))
        return self._metric.compute(predictions=predictions, references=labels)

    def _compute_final_fold_metrics(self):
        predictions, labels = self._cache_eval_pred
        predictions = np.argmax(predictions, axis=1)
        print(classification_report(labels, predictions))

        # logits, labels = eval_pred
        # predictions = np.argmax(logits, axis=-1)
        # precision, recall, f1, _ = precision_recall_fscore_support(
        #     labels, predictions, average="macro"
        # )
        # return {
        #     "final_fold_precision": precision,
        #     "final_fold_recall": recall,
        #     "final_fold_f1": f1
        # }

    def _run_fold(self, train_idx, val_idx, fold, results):
        print('Training fold ' + str(fold))
        train_fold = self._dataset.select(train_idx)
        val_fold = self._dataset.select(val_idx)
        model = AutoModelForSequenceClassification.from_pretrained(self._model, num_labels=2)
        if self._metric_for_best_model=='accuracy':
            gis=True
        else:
            gis=False
        training_args = TrainingArguments(
            output_dir=f"./results_fold_{fold}",
            eval_strategy="epoch", save_strategy="epoch", learning_rate=2e-5,
            per_device_train_batch_size=self._batch_size, per_device_eval_batch_size=self._batch_size,
            num_train_epochs=self._epochs, weight_decay=0.01,
            load_best_model_at_end=True, metric_for_best_model=self._metric_for_best_model,
            push_to_hub=False,greater_is_better=gis,
        )
        #metric_for_best_model="accuracy", greater_is_better=True
        trainer = Trainer(model=model, args=training_args, train_dataset=train_fold,
                          eval_dataset=val_fold, compute_metrics=self._compute_metrics,
                          callbacks=[EarlyStoppingCallback(early_stopping_patience=3)])
        trainer.train()
        fold_metrics = trainer.evaluate()
        results.append(fold_metrics)
        self._compute_final_fold_metrics()

    def _run(self, ds):
        print('Training (no validation)')
        #model = AutoModelForSequenceClassification.from_pretrained(self._model, num_labels=2)
        model = RobertaForSequenceClassification.from_pretrained(self._model, num_labels=2)
        training_args = TrainingArguments(
            output_dir=f"./results",
            eval_strategy="no",
            save_strategy="no", learning_rate=2e-5,
            per_device_train_batch_size=self._batch_size, per_device_eval_batch_size=self._batch_size,
            num_train_epochs=self._epochs, weight_decay=0.01,
            load_best_model_at_end=False, metric_for_best_model="accuracy", push_to_hub=False,
        )
        trainer = Trainer(model=model, args=training_args,
                          train_dataset=ds, compute_metrics=self._compute_metrics, )
        trainer.train()
        trainer.save_model("./results/final_model")

    def train(self):
        if self._skf is None:
            self._run(self._dataset)
        else:
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

fn1 = "drive/MyDrive/explorer/heavy/r0_n1000_curated.txt"
fn2 = "drive/MyDrive/explorer/heavy/prame.txt"

aa_seq_1 = prepare_input(fn1, 0)
aa_seq_2 = prepare_input(fn2, 1)

checker = SequenceSanityChecker([aa_seq_1, aa_seq_2])
rep=checker.create_std_report()
print(rep)

f=Features()
f.add(aa_seq_1)
f.add(aa_seq_2)


skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
abrt=AbRobertaTrainer(model="mogam-ai/Ab-RoBERTa", dataset=f.export_to_dataset(), skf=skf,
                epochs=10, batch_size=8)
abrt.train()