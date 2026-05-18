import os.path
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

class BatchedAbRobertaInterference():
    def __init__(self, model_path, model_name, seqs, batch_size):
        self._model_path = model_path
        self._model_name = model_name
        self._seqs = seqs
        self._batch_size = batch_size

    def run_batched_interference(self, out_path):
        seqsbatch = []
        for i in range(len(seqs)):
            seqsbatch.append(seqs[i])
            if len(seqsbatch) == self._batch_size:
                print('processing ' + str(i))
                inf = AbRobertaInterference(self._model_path, self._model_name, seqsbatch)
                result = inf.run_inference()
                out_fn=os.path.join(out_path, 'result_'  + str(i) + '.pkl')
                with open(out_fn, 'wb') as f:  # 'wb' means write-binary
                    pickle.dump(result, f)
                seqsbatch = []
        if len(seqsbatch) != 0:
            print('processing final batch...')
            inf = AbRobertaInterference(model_path, model_name, seqsbatch)
            result = inf.run_inference()
            out_fn=os.path.join(out_path, 'result_'  + str(len(seqsbatch) +  i) + '.pkl')
            with open(out_fn, 'wb') as f:  # 'wb' means write-binary
                pickle.dump(result, f)
        print('Done!')


def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    removed = out.remove_sequences(disallowed_text=['X','MISSING'])
    out = out.get_unique_sequences()
    return out

fn = "drive/MyDrive/explorer/heavy/r0_curated.txt"
fn = "C:/Nextera/div/ab_roberta/EXPLORER/heavy/r0_curated.txt"
aa_seq = prepare_input(fn, 0)
checker = SequenceSanityChecker([aa_seq])
rep=checker.create_std_report()
print(rep)

seqs=aa_seq.get_sequence_list()

model_path = "drive/MyDrive/explorer/heavy/final_model"
model_name = "mogam-ai/Ab-RoBERTa"

inf=BatchedAbRobertaInterference(model_path, model_name, seqs, 10000)
inf.run_batched_interference('./')

# seqsbatch=[]
# for i in range(len(seqs)):
#     seqsbatch.append (seqs[i])
#     if len(seqsbatch)==10000:
#         print('processing ' + str(i))
#         inf = AbRobertaInterference(model_path, model_name, seqsbatch)
#         result = inf.run_inference()
#         with open('r0_result.pkl' + str(i), 'wb') as f:  # 'wb' means write-binary
#             pickle.dump(result, f)
#         seqsbatch = []
# if len(seqsbatch)!=0:
#     print('processing final batch...')
#     inf = AbRobertaInterference(model_path, model_name, seqsbatch)
#     result = inf.run_inference()
#     with open('r0_result.pkl' + str(i+1), 'wb') as f:  # 'wb' means write-binary
#         pickle.dump(result, f)
# print('Done!')
# p=Parser(result)
# p.to_string()
#
# x=p.filter('LABEL_0', 0.9, True)
# p=Parser(x)
#
# print(p.to_string())

