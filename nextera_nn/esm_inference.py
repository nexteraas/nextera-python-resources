from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
import pickle


class EsmInterference():
    def __init__(self, model_path, model_name, seqs):
        self._model_path = model_path
        self._model_name = model_name
        self._seqs = seqs

    def run_inference(self, batch_size=16, device=0):
        model = AutoModelForSequenceClassification.from_pretrained(self._model_path, use_safetensors=True)
        tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        pipe = pipeline(task="text-classification", model=model, tokenizer=tokenizer, device=device)
        out = pipe(self._seqs, batch_size=batch_size)
        return out

class Parser():
    def __init__(self, data):
        self._data = data

    def print_head(self, n=10):
        for r in self.data:
            print(r)

    def filter(self, class_txt, threshold=0.5, above=True):
        i = -1
        out=[]
        for r in self._data:
            i+=1
            txt= r['label']
            if class_txt == txt:
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

    def to_string(self):
        print(self._data)


def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    removed = out.remove_sequences(disallowed_text=['X','MISSING'])
    out = out.get_unique_sequences()
    return out

fn = "C:/Nextera/div/ab_roberta/EXPLORER/curated/r0.txt"
aa_seq = prepare_input(fn, 0)
checker = SequenceSanityChecker([aa_seq])
rep=checker.create_std_report()
print(rep)

seqs=aa_seq.get_sequence_list()

model_path = "drive/MyDrive/explorer/final_model"
model_name = "facebook/esm2_t30_150M_UR50D"
inf=EsmInterference(model_path, model_name, seqs)
result = inf.run_inference()

with open('r0_result.pkl', 'wb') as f:  # 'wb' means write-binary
    pickle.dump(result, f)

p=Parser(result)
p.to_string()

x=p.filter('LABEL_0', 0.9, True)
p=Parser(x)

print(p.to_string())

