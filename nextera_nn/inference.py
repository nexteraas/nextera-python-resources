import torch
from transformers import (
    RobertaTokenizer, RobertaForSequenceClassification,
    RobertaModel, AutoTokenizer, AutoModelForSequenceClassification,
)

model_name = "facebook/esm2_t30_150M_UR50D"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def run_inference():
    num_labels=2
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    fn = "C:/Nextera/div/ab_roberta/mage_prame_vs_tus/esm_prame_hs.pt"
    model.load_state_dict(torch.load(fn, weights_only=True))
    text='ETTLTQSPGTLSLSPGERATLSCRASQSVYNNLAWYQQKPGQAPRLLIYGASTRATGIPARFSGSGSGTEFSLTISSLQSEDFALYSCQQYNNWPYTFGQGTKVEIKQVQLVQSGAEVKKPGSSVKVSCKASGGTFSSYAISWVRQAPGQGLEWMGGIIPIFGTANYAQKFQGRVTITADESTSTVYMELSSLRSEDTAVYYCARAVGYCSGGSCSDFDYWGQGTLVTVSS'
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    print(predicted_class_id)


run_inference()