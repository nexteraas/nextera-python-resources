import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse

from nextera_utils.docker_interop import DockerInterop


class SamplingProbabilitiesPlotter():

    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    def plot_overview(self, out_fn):
        plt.figure()
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.5)
        self._data_df.sort_values(by=self._data_df.columns[0], ascending=False, inplace=True)
        x=self._data_df.iloc[:,0]
        plt.xticks(rotation=45)
        y=self._data_df.iloc[:,1]
        sns.scatterplot(x,y)
        plt.xlabel("Sequence ids")
        plt.ylabel("No. of samples")
        if self._debug_key is None:
            plt.savefig(out_fn)
        else:
            plt.show()

    def plot_details(self, out_fn):
        plt.figure()
        plt.tight_layout()
        self._data_df.sort_values(by=self._data_df.columns[0], ascending=True, inplace=True)
        x=self._data_df.index
        y=self._data_df.iloc[:,0]
        sns.scatterplot(x,y)
        plt.xlabel("No. of samples")
        plt.ylabel("Prob. of finding the sequence")
        if self._debug_key is None:
            plt.savefig(out_fn)
        else:
            plt.show()