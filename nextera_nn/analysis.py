from inference_result import InferenceResult, InferenceResults
import matplotlib.pyplot as plt
from aa_sequence_map import AaSequenceMap
from inference_parser import InferenceParser
from inference_parser import Plotter


def prepare_input(fn, tag):
    out = AaSequenceMap(fn, tag=tag)
    removed = out.remove_sequences(disallowed_text=['X','MISSING'])
    out = out.get_unique_sequences()
    return out

fn_seqs="C:/Nextera/div/ab_roberta/EXPLORER/heavy/r0_curated.txt"
seqs=prepare_input(fn_seqs,0)
print(len(seqs.get_sequence_list()))

fn="C:/Nextera/div/ab_roberta/EXPLORER/heavy/result_final.pkl"
p=InferenceParser.instantiate(fn)
i_dict=p.filter(class_txt='LABEL_1', threshold=0.50, above=True)
p1=InferenceParser(i_dict)
i_dict=p.filter(class_txt='LABEL_0', threshold=0.90, above=True)
p2=InferenceParser(i_dict)
top_2=p2.get_sorted_list(inc=False)
top_2=top_2[0:len(p1)]
p2=InferenceParser(top_2)
print(str(len(p2)))

plotter=Plotter()
plotter.plot(parsers=[p1, p2], colors=['blue', 'green'], labels=['PRAME', 'R0'] )

#seqs_list=seqs.get_sequence_list()
extracted_seqs=InferenceParser.extract_sequences(i_dict, seqs)
aa_map=AaSequenceMap(fn=None, sequences=extracted_seqs)
aa_map.write("C:/Nextera/div/ab_roberta/EXPLORER/heavy/extracted_r0_n150000_seqs.txt")
print('d')

exit(0)








def plot_inference_results_2(fns, colors, labels, cutoff, above, prob0, inc, sort_on_prob0):
    c_index = 0
    for fn in fns:
        ifrs = InferenceResults()
        ifrs.parse_results(fn)
        tmp = ifrs.filter(cutoff, above, prob0)
        ifrs = InferenceResults(tmp)
        results = ifrs.get_sorted_list(inc, sort_on_prob0)
        _plot_inference_results(results, colors[c_index], labels[c_index])
        c_index += 1
    plt.legend(loc='upper right')
    plt.show()

def _plot_inference_results(results, color, label):
    y = []
    x = []
    i=0
    for ifr in results:
        x.append(i)
        i+=1
        y.append(ifr[1].prob0)
    plt.scatter(x, y, c=color, s=1, label=label)

def plot_inference_results(fns, colors, cutoff, above, prob0, inc, sort_on_prob0):
    y = []
    x = []
    cs = []
    c_index = 0
    for fn in fns:
        ifrs = InferenceResults()
        ifrs.parse_results(fn)
        tmp = ifrs.filter(cutoff, above, prob0)
        ifrs = InferenceResults(tmp)
        lst = ifrs.get_sorted_list(inc, sort_on_prob0)
        i = 0
        for ifr in lst:
            x.append(i)
            i += 1
            y.append(ifr[1].prob0)
            cs.append(colors[c_index])
        i = 0
        c_index += 1
    plt.scatter(x, y, c=cs, s=1)
    plt.show()


fns=["C:/Nextera/div/ab_roberta/mage_prame_vs_tus/out/mage_indices",
     "C:/Nextera/div/ab_roberta/mage_prame_vs_tus/out/prame_indices"]
colors=['red','blue']
plot_inference_results_2(fns, colors, ['MAGE', 'PRAME'], 0.0,True, True, False, True)
#plot_inference_results(fns, colors, 0.0, True, True, False, True)

