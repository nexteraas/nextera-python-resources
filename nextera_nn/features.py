import random
import copy
from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
import pandas as pd
from datasets import Dataset
from sklearn.model_selection import StratifiedKFold
import numpy as np


class Features(object):
    def __init__(self):
        self._aa_sequence_maps = {}

    def add(self, aa_sequence_map, key=None):
        if key is None:
            k=aa_sequence_map.get_fn()
        else:
            k=key
        self._aa_sequence_maps[k] = aa_sequence_map

    def balance(self, count=None, mode='copy_existing'):
        if count is None:
            counts=[]
            for aa_map in self._aa_sequence_maps.values():
                counts.append(len(aa_map.get_sequences()))
            count=max(counts)
        for aa_map in self._aa_sequence_maps.values():
            self._balance(aa_map, count, mode)

    def _balance(self, aa_seq_map, count, mode):
        if mode != 'copy_existing':
            raise Exception(f"Illegal mode: {mode}")
        count_aa_seq_map=len(aa_seq_map.get_sequences())
        if count_aa_seq_map == count:
            return
        if count_aa_seq_map > count:
            keys_list = list(aa_seq_map.get_sequences().keys())
            n = count_aa_seq_map- count
            random_keys = random.sample(keys_list, k=n)
            for k in random_keys:
                del aa_seq_map.get_sequences()[k]
        else:
            keys_list = list(aa_seq_map.get_sequences().keys())
            n=count-count_aa_seq_map
            random_keys = random.choices(keys_list, k=n)
            new_seqs={}
            for c, k in enumerate(random_keys):
                seq = aa_seq_map.get_sequences()[k]
                new_seq = copy.deepcopy(seq)
                new_header = k + str(c)
                new_seqs[new_header] = new_seq
            for h, s in new_seqs.items():
                aa_seq_map.get_sequences()[h] = s

    def split_train_test(self, train_proportion=0.75):
        if (train_proportion<=0) or (train_proportion>=1):
            raise Exception(f"Illegal train proportion: {train_proportion}")
        train_out=Features()
        test_out=Features()
        for aa_map in self._aa_sequence_maps.values():
            l=len(aa_map.get_sequences())
            train_n=int(l*train_proportion)
            keys_list=list(aa_map.get_sequences().keys())
            train_keys=random.sample(keys_list, train_n)
            train_seqs={}
            test_seqs={}
            for k in keys_list:
                if k in train_keys:
                    train_seqs[k]=aa_map.get_sequences()[k]
                else:
                    test_seqs[k] = aa_map.get_sequences()[k]
            train_map=AaSequenceMap(fn=aa_map.get_fn(), sequences=train_seqs, tag=aa_map.get_tag())
            test_map=AaSequenceMap(fn=aa_map.get_fn(), sequences=test_seqs, tag=aa_map.get_tag())
            train_out.add(train_map)
            test_out.add(test_map)
        return train_out, test_out

    def export_to_dataframe(self, randomize=True):
        out=None
        for aa_map in self._aa_sequence_maps.values():
            seqs=aa_map.get_sequence_list()
            df=pd.DataFrame(seqs, columns=['sequence'])
            t = aa_map.get_tag()
            if not isinstance(t, int):
                raise Exception(f"Tag property is not int: {t}")
            df['label'] = t
            if out is None:
                out = df
            else:
                out = pd.concat([out, df], ignore_index=True)
        if randomize:
            out = out.sample(frac=1).reset_index(drop=True)
        return out

    def export_to_dataset(self, randomize=True):
        df=self.export_to_dataframe(randomize)
        out = Dataset.from_pandas(df)
        return out

    def iterate_k_fold_validation(self, exec_func,epochs=3, n_splits=5, shuffle=True, random_state=42):
        skf = StratifiedKFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
        ds=self.export_to_dataset(randomize=True)
        labels = np.array(ds["label"])
        for fold, (train_idx, val_idx) in enumerate(skf.split(ds, labels)):
            print(f"--- Fold {fold + 1}/{n_splits} ---")
            train_ds = ds.select(train_idx)
            val_ds = ds.select(val_idx)
            exec_func(train_ds, val_ds, epochs)

        # performance_metrics = []
        # for fold_idx, (train_indices, val_indices) in enumerate(skf.split(X, y)):
        #     train_dataset = YourCustomDataset(X[train_indices], y[train_indices])
        #     val_dataset = YourCustomDataset(X[val_indices], y[val_indices])
        #     model = RobertaForSequenceClassification.from_pretrained('roberta-base', num_labels=num_labels)
        #     training_args = TrainingArguments(
        #         output_dir=f'./results_fold_{fold_idx + 1}',
        #     )
        #     trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=val_dataset, )
        #     trainer.train()
        #     metrics = trainer.evaluate()
        #     performance_metrics.append(metrics['eval_accuracy'])  # Example
        # average_performance = np.mean(performance_metrics)
        # print(f"Average validation accuracy across all folds: {average_performance}")


