import pickle
from aa_sequence_map import AaSequenceMap


class InferenceParser():
    def __init__(self, data):
        self._data = data

    def head(self, n=10):
        out = ""
        i = 0
        for r in self._data:
            out += str(r) + "\n"
            print(r)
            if n is not None:
                if i >= n:
                    break
            i += 1
        return out

    def __len__(self):
        return len(self._data)

    def filter(self, class_txt=None, threshold=0.5, above=True):
        i = -1
        out = []
        for r in self._data:
            i += 1
            txt = r['label']
            if class_txt == txt or class_txt is None:
                val = r['score']
                if above:
                    if val >= threshold:
                        r['index'] = i
                        out.append(r)
                else:
                    if val <= threshold:
                        r['index'] = i
                        out.append(r)
        return out

    def __str__(self):
        out = str(len(self._data)) + ' items'
        return out

    @staticmethod
    def extract_sequences(indexed_dict, aa_seqs_map):
        #indexed_dict is assumed produced by the InferenceParser.filter method
        out = {}
        s_keys = list(aa_seqs_map.get_sequences().keys())
        for r in indexed_dict:
            i = r['index']
            k = s_keys[i]
            sequence = aa_seqs_map.get_sequences()[k]
            out[k] = sequence
        return out

    @staticmethod
    def instantiate(fn):
        with open(fn, 'rb') as file:
            data = pickle.load(file)
            out = InferenceParser(data)
        return out




fn="C:/Nextera/div/ab_roberta/EXPLORER/heavy/result_final.pkl"
p=InferenceParser.instantiate(fn)
i_dict=p.filter(class_txt='LABEL_1', threshold=0.99, above=True)
p=InferenceParser(i_dict)
print(str(len(p)))
fn_seqs="C:/Nextera/div/ab_roberta/EXPLORER/heavy/r0.txt"
seqs=AaSequenceMap(fn_seqs)
#seqs_list=seqs.get_sequence_list()
extracted_seqs=InferenceParser.extract_sequences(i_dict, seqs)
aa_map=AaSequenceMap(fn=None, sequences=extracted_seqs)
aa_map.write("C:/Nextera/div/ab_roberta/EXPLORER/heavy/extracted_r0_seqs.txt")
print('d')