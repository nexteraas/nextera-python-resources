import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker
from textwrap import wrap
from nextera_utils.docker_interop import DockerInterop

class DiversityPlotter:
    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key=DockerInterop.get_instance().get_debug_key()

    def plot(self, out_fn):
        fig, axs = plt.subplots(2, 2)
        self._plot_axis(axs[0, 0], 'ENS-IGHV', False)
        self._plot_axis(axs[0, 1], 'ENS-IGLV', False)
        self._plot_axis(axs[1, 0], 'ENS-IGHJ', False)
        self._plot_axis(axs[1, 1], 'ENS-IGLJ', False)
        self.plot_pannings(fig)
        plt.tight_layout()
        # plt.savefig(out_fn)
        if self._debug_key is None:
            plt.savefig(out_fn)
        else:
            plt.show()

    def plot_pannings(self, fig):
        xlabels = list(self._data_df.index.values)
        xlabels = ", ".join(xlabels)
        xlabels = 'Diversities for pannings: ' + xlabels
        xlabels = "\n".join(wrap(xlabels,))
        fig.suptitle(xlabels, fontsize=10)

    def _plot_axis(self, axis, colName, inc_x_ticks):
        xlabels=list(self._data_df.index.values)
        values = list(self._data_df[colName])
        axis.xaxis.set_major_locator(ticker.MultipleLocator(1))
        axis.tick_params(axis='x', which='major', labelsize=4)
        if inc_x_ticks:
            axis.plot(xlabels, values, linestyle='dotted')
        else:
            axis.plot(values, linestyle='dotted')
            #axis.set_xticks([])
            axis.tick_params(labelbottom=False)
        axis.set_title(colName, fontsize=10)
