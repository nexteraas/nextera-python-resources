import torch
from pathlib import Path
import os
from aa_sequence_map import AaSequenceMap
from transformers import (
   AutoTokenizer, AutoModelForSequenceClassification,
)

class InferenceResult():
    def __init__(self, prob0, prob1):
        self.prob0 = prob0
        self.prob1 = prob1

class InferenceResults():
    def __init__(self, map=None):
        self._map = map

    def parse_results(self, fn):
        self._map = {}
        path_only = Path(fn).parent
        fn_filename = Path(fn).stem
        files_and_dirs = os.listdir(path_only)
        for f in files_and_dirs:
            # if os.path.isfile(f):
            filename = Path(f).stem
            if filename.startswith(fn_filename):
                res = self._parse_result(os.path.join(path_only, filename))
                self._map.update(res)

    def _parse_result(self, fn):
        out = {}
        with open(fn, 'r') as file:
            for line in file:
                line = line.strip()
                fields = line.split('\t')
                id = fields[0]
                probs = fields[1]
                i1 = probs.find('[')
                i2 = probs.find(']')
                probs = probs[i1 + 1:i2]
                probs = probs.split(",")
                c0 = float(probs[0].strip())
                c1 = float(probs[1].strip())
                ifr = InferenceResult(c0, c1)
                out[id] = ifr
        return out

    def get_sorted_list(self, inc=True, sort_on_prob0=True):
        if sort_on_prob0:
            out = sorted(self._map.items(), key=lambda item: item[1].prob0)
        else:
            out = sorted(self._map.items(), key=lambda item: item[1].prob1)
        if not inc:
            out.reverse()
        return out

    def filter(self, cutoff, above=True, prob0=True):
        out={}
        for k, v in self._map.items():
            if prob0:
                tmp = v.prob0
            else:
                tmp = v.prob1
            if above:
                if tmp >= cutoff:
                    out[k]=v
            else:
                if tmp < cutoff:
                    out[k]=v
        return out



model_name = "facebook/esm2_t30_150M_UR50D"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def run_inference(model_fn, num_labels, seqs, out_fn, batch_size=9):
    seq_list = seqs.get_sequence_list()
    id_list = seqs.get_id_list()
    from_i = 0
    batch=0
    while True:
        to_i = from_i + batch_size
        if to_i >= len(seq_list):
            to_i = len(seq_list)
        seq_batch=seq_list[from_i:to_i]
        id_batch=id_list[from_i:to_i]
        predictions = run_inference_batch(model_fn, num_labels, seq_batch)
        batch_fn=out_fn + str(batch)
        save_predictions(predictions, id_batch, batch_fn)
        from_i+=batch_size
        if from_i >= len(seq_list):
            break
        batch+=1


def run_inference_batch(model_fn, num_labels, seqs):
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.load_state_dict(torch.load(model_fn, weights_only=True))
    model.to(device)
    inputs = tokenizer(
        seqs,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )
    inputs = inputs.to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    # 5. Process logits (apply softmax to get probabilities)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return predictions


def save_predictions(predictions, ids, fn):
    with open(fn, 'w') as f:
        id_i=0
        for i in predictions:
            id=ids[id_i]
            id_i+=1
            f.write(f"{id}\t{i}\n")


def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    l = len(out.get_sequences())
    out.remove_sequences(disallowed_text=['X', 'MISSING'])
    out=out.get_unique_sequences()
    if l!=len(out.get_sequences()):
        print ('Illegal sequences present in input; aborting!')
        return None
    return out


fn="C:/Nextera/div/ab_roberta/mage_prame_vs_tus/out/prame_indices"
ifrs=InferenceResults()
ifrs.parse_results(fn)
lst=ifrs.get_sorted_list(False, True)
c=lst

x=ifrs.filter(0.5, True, True)
ifrs=InferenceResults(x)
lst=ifrs.get_sorted_list(False, True)
exit(0)

fn = "C:/Nextera/div/ab_roberta/mage_prame_vs_tus/r0.txt"
model_fn = "drive/MyDrive/esm_prame_hs.pt"

seqs = prepare_input(fn, 0)
if seqs is None:
    exit(1)
out_fn = "drive/MyDrive/prame_indices"
indices = run_inference(model_fn, 2, seqs, out_fn, batch_size=9)


