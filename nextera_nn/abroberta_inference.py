from transformers import AutoTokenizer, RobertaForSequenceClassification
from transformers import pipeline
from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker
import pickle


class AbRobertaInterference():
    def __init__(self, model_path, model_name, seqs):
        self._model_path = model_path
        self._model_name = model_name
        self._seqs = seqs

    def run_inference(self, batch_size=16, device=0):
        model = RobertaForSequenceClassification.from_pretrained(self._model_path, use_safetensors=True)
        tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        pipe = pipeline(task="text-classification", model=model, tokenizer=tokenizer, device=device,
                        max_length=150, truncation=True)
        out = pipe(self._seqs, batch_size=batch_size)
        return out



def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    removed = out.remove_sequences(disallowed_text=['X','MISSING'])
    out = out.get_unique_sequences()
    return out

fn = "C:/Nextera/div/ab_roberta/EXPLORER/curated/r0_n1000.txt"
aa_seq = prepare_input(fn, 0)
checker = SequenceSanityChecker([aa_seq])
rep=checker.create_std_report()
print(rep)

seqs=aa_seq.get_sequence_list()

model_path = "drive/MyDrive/explorer/final_model"
model_name = "mogam-ai/Ab-RoBERTa"

seqsbatch=[]
for i in range(len(seqs)):
    seqsbatch.append (seqs[i])
    if len(seqsbatch)==10000:
        inf = AbRobertaInterference(model_path, model_name, seqsbatch)
        result = inf.run_inference()
        with open('r0_result.pkl' + str(i), 'wb') as f:  # 'wb' means write-binary
            pickle.dump(result, f)
        seqsbatch = []
if len(seqsbatch)!=0:
    inf = AbRobertaInterference(model_path, model_name, seqsbatch)
    result = inf.run_inference()
    with open('r0_result.pkl' + str(i+1), 'wb') as f:  # 'wb' means write-binary
        pickle.dump(result, f)

# p=Parser(result)
# p.to_string()
#
# x=p.filter('LABEL_0', 0.9, True)
# p=Parser(x)
#
# print(p.to_string())

