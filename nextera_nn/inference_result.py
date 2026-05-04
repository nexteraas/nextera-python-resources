from pathlib import Path
import os


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

