from builtins import object
import numpy as np
import matplotlib.pyplot as plt
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils
from matplotlib import transforms


class PrimerEffectsPlotter(object):
    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key=DockerInterop.get_instance().get_debug_key()
        self._max_lines_pr_plot=5

    def plot(self, out_fn):
        if self._data_df.empty: return
        genes = self._data_df.Gene.unique()
        no_of_plots = len(genes) / self._max_lines_pr_plot
        no_of_plots = int(no_of_plots) + 1
        fig, axs = plt.subplots(nrows=no_of_plots, ncols=1)
        index=0
        for i in range(0, no_of_plots, 1):
            for j in range(0, self._max_lines_pr_plot):
                if index+1>len(genes):
                    break
                gene = genes[index]
                gene_df = self._data_df.loc[self._data_df['Gene'] == gene]
                n = gene_df.iloc[0]['n']
                l = gene + ' (n=' + str(n) + ')'
                ax = self.get_axis(i, axs)
                # ax.set_xlim([1, None])
                # ax.set_ylim([0, None])
                tr = transforms.offset_copy(ax.transData, fig=fig, x=0.0, y=-1.5, units='points')
                ax.plot(gene_df['Index'], gene_df['Frequency'], linestyle='-', label=l) # marker='o'
                ax.set_xlim(left=1)
                ax.set_ylim(bottom=0)
                ax.legend(loc='best', ncol=self._max_lines_pr_plot, prop={'size': 6})
                index+=1
        utils.saveFigure(out_fn)

    def get_axis(self, index, axes):
        t = type(axes)
        if str(t) =='<class \'numpy.ndarray\'>':
            return axes[index]
        else:
            return axes

