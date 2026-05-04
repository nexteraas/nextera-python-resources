from inference_result import InferenceResult, InferenceResults
import matplotlib.pyplot as plt



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
plot_inference_results(fns, colors, 0.0, True, True, False, True)

