from igfold import IgFoldRunner
from igfold.refine.pyrosetta_ref import init_pyrosetta


import torch
# Temporarily modify the default weights_only behavior
original_load = torch.load
def custom_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_load(*args, **kwargs)
torch.load = custom_load


class IgFoldPredictor(object):
    def __init__(self, refine=True, renum=True):
        print('Entered IgFoldPredictor and loaded stuff...')
        self._refine = refine
        self._renum = renum
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
        igfold.fold(pred_pdb, sequences=sequences, do_refine=self._refine, do_renum=self._renum)
