from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from aa_sequence_map import AaSequenceMap
from  sanity_checker import SequenceSanityChecker


class EsmInterference():
    def __init__(self, model_path, model_name, seqs):
        self._model_path = model_path
        self._model_name = model_name
        self._seqs = seqs

    def run_inference(self):
        model = AutoModelForSequenceClassification.from_pretrained(self._model_path, use_safetensors=True)
        tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        pipe = pipeline(task="text-classification", model=model, tokenizer=tokenizer)
        out = pipe(self._seqs)
        return out

# seqs=[]
#
# seqs.append("TQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSYSTLPYTFGQGTKVEIKQLVQSGAEVKKPGASVKVSCKASGYTFTSYGISWVRQAPGQGLEWMGWISAYNGNTNYAQKLQGRVTMTTDTSTSTAYMELRSLRSDDTAVYYCARVYCSSTSCYDYAEYFQHWGQGTLVTVSS")
# seqs.append("TQSPSSLSASVGDRVTITCQASQDISNYLNWYQQKPGKAPKLLIYDASNLETGVPSRFSGSGSGTDFTFTISSLQPEDIATYYCLQHNSYLPTFGGGTKVEIKQLVQSGAEVKKPGSSVKVSCKASGGTFSSYAISWVRQAPGQGLEWMGGIIPIFGTANYAQKFQGRVTITADESTSTAYMELSSLRSEDTAVYYCARTIGHDLPDAFDIWGQGTMVTVSS")
# seqs.append("TQSPSSLSASVGDRVTITCQASQDISEYLNWYQQKPGKAPKVLISEASNLETGVPSRFGGSGSGTDFTFTISSLQPEDIATYYCQQYDDLPITFGQGTRLEIKQLQQWGAGLLKPSETLSLTCAVYGGSFSGYYWSWIRQPPGKGLEWIGEINHSGSTNYNPSLKSRVTISVDTSKNQFSLKLSSVTAADTAVYYCARGGYSYGYDYWGQGTLVTVSS")
# seqs.append("TQSPATLSVSPGERATLSCRASQSVSSNLAWYQQKPGQAPRLLIYGASTRATGIPARFSGSGSGTEFTLTISSLQSEDFAVYYCQQYNNWPPYTFGQGTKLEIKQLVQSGAEVKKPGASVKVSCKASGYTFTSYGISWVRQAPGQGLEWMGWISAYNGNTNYAQKLQGRVTMTTDTSTSTAYMELRSLRSDDTAVYYCARDLDSYSYYFDYWGQGTLVTVSS")
#

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

print(result)

