import torch
from aa_sequence_map import AaSequenceMap
from transformers import (
    RobertaTokenizer, RobertaForSequenceClassification,
    RobertaModel, AutoTokenizer, AutoModelForSequenceClassification,
)

model_name = "facebook/esm2_t30_150M_UR50D"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def run_inference(model_fn, num_labels, seqs, out_fn, batch_size=9):
    seq_list = seqs.get_sequence_list()
    id_list = seq_list.get_sequence_ids()
    from_i = 0
    batch=0
    while True:
        seq_batch=seq_list[from_i:from_i+batch_size-1]
        predictions = run_inference_batch(model_fn, num_labels, seq_batch)
        batch_fn=out_fn + str(batch)
        save_predictions(predictions, id_list, batch_fn)
        from_i+=batch_size
        batch+=1



def run_inference_batch(model_fn, num_labels, seqs):
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.load_state_dict(torch.load(model_fn, weights_only=True))
    model.to(device)
    # str1 = "EIVLTQSPATLSVSPGERATLSCRASQSVNSNLAWYQQKPGQAPRLLIYGASTRATGIPARFSGSGSGTEFTLTISRLEPEDFAVYYCQQYDNWLSPTFGGGTKVEIKQVQLQESGPGLVKPSGTLSLTCAVSGGSISSSNWWSWVRQPPGKGLEWIGEIYHSGSTNYNPSLKSRVTISVDKSKNQFSLKLSSVTAADTAVYYCASGGADGDYYAFDIWGQGTMVTVSS"
    # str2 = "ETTLTQSPGTLSLSPGERATLSCRASQSVYNNLAWYQQKPGQAPRLLIYGASTRATGIPARFSGSGSGTEFSLTISSLQSEDFALYSCQQYNNWPYTFGQGTKVEIKQVQLVQSGAEVKKPGSSVKVSCKASGGTFSSYAISWVRQAPGQGLEWMGGIIPIFGTANYAQKFQGRVTITADESTSTVYMELSSLRSEDTAVYYCARAVGYCSGGSCSDFDYWGQGTLVTVSS"
    # in_list = [str1, str2]

    # 3. Tokenize them together
    lst=seqs.get_sequence_list()
    inputs = tokenizer(
        lst,
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
            f.write(f"{id}\n{i}\n")

def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    l = len(out.get_sequences())
    out.remove_sequences(disallowed_text=['X', 'MISSING'])
    out=out.get_unique_sequences()
    if l!=len(out.get_sequences()):
        print ('Illegal sequences present in input; aborting!')
        return None
    return out

fn = "C:/Nextera/div/ab_roberta/mage_prame_vs_tus/r0.txt"
model_fn = "drive/MyDrive/esm_prame_hs.pt"

seqs = prepare_input(fn, 0)
if seqs is None:
    exit(1)
out_fn = "drive/MyDrive/prame_indices"
indices = run_inference(model_fn, 2, seqs, out_fn, batch_size=9)

save_predictions(indices, out_fn)
