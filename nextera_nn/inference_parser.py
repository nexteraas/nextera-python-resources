import pickle
import matplotlib.pyplot as plt


class InferenceParser():
    def __init__(self, data):
        self._data = data

    def head(self, n=10):
        out = ""
        i = 0
        for r in self._data:
            out += str(r) + "\n"
            print(r)
            if n is not None:
                if i >= n:
                    break
            i += 1
        return out

    def __len__(self):
        return len(self._data)

    def filter(self, class_txt=None, threshold=0.5, above=True):
        i = -1
        out = []
        for r in self._data:
            i += 1
            txt = r['label']
            if class_txt == txt or class_txt is None:
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

    def get_sorted_list(self, inc=True):
        out = sorted(self._data, key=lambda item: item['score'])
        if not inc:
            out.reverse()
        return out

    def __str__(self):
        out = str(len(self._data)) + ' items'
        return out

    @staticmethod
    def extract_sequences(indexed_dict, aa_seqs_map):
        #indexed_dict is assumed produced by the InferenceParser.filter method
        out = {}
        s_keys = list(aa_seqs_map.get_sequences().keys())
        for r in indexed_dict:
            i = r['index']
            k = s_keys[i]
            sequence = aa_seqs_map.get_sequences()[k]
            out[k] = sequence
        return out

    @staticmethod
    def instantiate(fn):
        with open(fn, 'rb') as file:
            data = pickle.load(file)
            out = InferenceParser(data)
        return out

class Plotter():
    def __init__(self, x_axis_unit="clones", y_axis_unit="Probability", property='score', legend_loc='upper right'):
        self._x_axis_unit = x_axis_unit
        self._y_axis_unit = y_axis_unit
        self._property = property
        self._legend_loc = legend_loc

    def plot(self, parsers, colors=None, labels=None, inc=False):
        c_index = 0
        l_index = 0
        for parser in parsers:
            if colors is None:
                color='blue'
            else:
                color=colors[c_index]
                c_index+=1
            if labels is None:
                label=None
            else:
                label=labels[l_index]
                l_index+=1
            self._plot(parser, color, label, inc)
        if self._legend_loc is not None:
            plt.legend(loc=self._legend_loc)
        plt.xlabel(self._x_axis_unit)
        plt.ylabel(self._y_axis_unit)
        plt.show()

    def _plot(self,parser, color, label, inc):
        y = []
        x = []
        lst = parser.get_sorted_list(inc)
        i = 0
        for ifr in lst:
            x.append(i)
            i += 1
            y.append(ifr[self._property])
        i = 0
        if label is None:
            plt.scatter(x, y, c=color, s=1)
        else:
            plt.scatter(x, y, c=color, s=1, label=label)

