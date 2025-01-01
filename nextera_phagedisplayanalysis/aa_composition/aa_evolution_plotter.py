from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
import nextera_utils.utils as utils
from nextera_utils.docker_interop import DockerInterop
import numpy as np


class AaEvolutionPlotter():

    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    def plot(self, out_fn):
        if self._data_df.empty: return
        plt.figure()
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        #ax.box(False)

        plt.tight_layout()
        max_x = self._data_df['Position'].max() + 1
        plt.xlim([0, max_x])
        plt.xticks(np.arange(0, max_x, 1.0))
        max_y = self._data_df['Mean increase'].max()
        min_y = self._data_df['Mean increase'].min()
        if max_y>1:
            plt.ylim(1, max_y)
        else:
            plt.ylim(min_y, 1)
        for index, row in self._data_df.iterrows():
            aa_color=self._get_aa_group_color(row["Aa group"])
            plt.text(row["Position"], row["Mean increase"], row["Kmer"], color=aa_color, fontweight='bold',
                     verticalalignment = 'center', horizontalalignment = 'center')
        utils.saveFigure(out_fn)

    def _get_aa_group_color(self, group):
        if group=='Positive':
            return 'Blue'
        elif group=='Negative':
            return 'Red'
        elif group=='Polar':
            return 'Purple'
        elif group == 'Nonpolar':
            return 'Grey'
        elif group == 'Aromatic':
            return 'Green'
        return 'Black'
