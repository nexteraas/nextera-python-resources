import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from textwrap import wrap
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils


class DiversityPlotter:

    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key=DockerInterop.get_instance().get_debug_key()

    def plot_peptide(self, out_fn):
        if self._data_df.empty: return
        plt.figure()
        for index, row in self._data_df.iterrows():
            plt.plot(row, linestyle='dotted', label=index)
        plt.legend()
        plt.tight_layout()
        utils.saveFigure(out_fn)

    def plot_ir(self, out_fn):
        if self._data_df.empty: return
        plt.figure()
        fig, axs = plt.subplots(2, 2)
        col_names=self._infer_colnames()
        self._plot_axis(axs[0, 0], col_names[0], False)
        self._plot_axis(axs[0, 1], col_names[1], False)
        self._plot_axis(axs[1, 0], col_names[2], False)
        self._plot_axis(axs[1, 1], col_names[3], False)
        self._plot_pannings_ir(fig)
        plt.tight_layout()
        utils.saveFigure(out_fn)

    def _infer_colnames(self):
        out = []
        if 'ENS [chain1-V]' in self._data_df:
            out.append('ENS [chain1-V]')
            out.append('ENS [chain2-V]')
            out.append('ENS [chain1-J]')
            out.append('ENS [chain2-J]')
        else:
            out.append('ENS [chain1-CDR3 length]')
            out.append('ENS [chain2-CDR3 length]')
            out.append('ENS [chain1+2 CDR3 length]')
            out.append('ENS [chain1+2 CDR3 length]')
        return out

    def _plot_pannings_ir(self, fig):
        xlabels = list(self._data_df.index.values)
        xlabels = ", ".join(xlabels)
        xlabels = 'Diversities for pannings: ' + xlabels
        xlabels = "\n".join(wrap(xlabels,))
        fig.suptitle(xlabels, fontsize=10)

    def _plot_axis(self, axis, col_name, inc_x_ticks):
        xlabels = list(self._data_df.index.values)
        values = list(self._data_df[col_name])
        axis.xaxis.set_major_locator(ticker.MultipleLocator(1))
        axis.tick_params(axis='x', which='major', labelsize=4)
        if inc_x_ticks:
            axis.plot(xlabels, values, linestyle='dotted')
        else:
            axis.plot(values, linestyle='dotted')
            #axis.set_xticks([])
            axis.tick_params(labelbottom=False)
        axis.set_title(col_name, fontsize=10)

