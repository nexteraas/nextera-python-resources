from igfold import IgFoldRunner
from igfold.refine.pyrosetta_ref import init_pyrosetta

class IgFoldPredictor(object):
    def __init__(self):
        print('Entered IgFoldPredictor and loaded stuff...')
        init_pyrosetta()

    def predict(self, sequences, out_fn):
        hs = sequences.iloc[0]['chain2']
        ls = sequences.iloc[0]["chain1"]
        sequences = {
            "H": hs.upper(),
            "L": ls.upper()
        }
        pred_pdb = out_fn
        igfold = IgFoldRunner()
        print('out:' + pred_pdb)
        print('H:' + sequences["H"])
        print('L:' + sequences["L"])
        igfold.fold(pred_pdb, sequences=sequences, do_refine=False, do_renum=False)
