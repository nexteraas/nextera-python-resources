import random
import copy
from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
import pandas as pd
from datasets import Dataset


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
            train_map=AaSequenceMap(fn=aa_map.get_fn(), sequences=train_seqs)
            test_map=AaSequenceMap(fn=aa_map.get_fn(), sequences=test_seqs)
            train_out.add(train_map)
            test_out.add(test_map)
        return train_out, test_out

    def export_to_dataframe(self):
        out=None
        for aa_map in self._aa_sequence_maps.values():
            seqs=aa_map.get_sequence_list()
            df=pd.DataFrame(seqs, columns=['sequence'])
            df['class'] = aa_map.get_tag()
            if out is None:
                out = df
            else:
                out = pd.concat([out, df], ignore_index=True)
        return out

    def export_to_dataset(self):
        df=self.export_to_dataframe()
        out = Dataset.from_pandas(df)
        return out


imp_specific = AaSequenceMap("C:/Nextera/div/ab_roberta/prame_specific_seqs.txt")
#imp_specific=FastaImporter("C:/Nextera/div/ab_roberta/test.fa", True, True)
removed1=imp_specific.remove_sequences(disallowed_aas=['X'])
imp_background=AaSequenceMap("C:/Nextera/div/ab_roberta/r0_n_250.txt")
imps=[imp_specific, imp_background]
checker= SequenceSanityChecker(imps)
checker.check_aas()
max1=checker.get_max_lengths(imp_specific)
max2=checker.get_max_lengths(imp_background)
aacount1=checker.check_unique_aa_counts(position_from=-2, position_to=None, aa_sequence_map=imp_specific)
aacount2=checker.check_unique_aa_counts(position_from=-2, position_to=None, aa_sequence_map=imp_background)

f=Features()
f.add(imp_specific)
f.add(imp_background)
#f.balance()
train_f, test_f=f.split_train_test()
df=9