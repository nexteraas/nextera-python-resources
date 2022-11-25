from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
import nextera_utils.utils as utils
from nextera_utils.docker_interop import DockerInterop


class SamplingProbabilitiesPlotter():

    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    def plot_overview(self, out_fn):
        if self._data_df.empty: return
        plt.figure()
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.5)
        self._data_df.sort_values(by=self._data_df.columns[1], ascending=False, inplace=True)
        plt.xticks(rotation=45)
        col0 = self._data_df.columns[0]
        col1 = self._data_df.columns[1]
        sns.scatterplot(data=self._data_df, x=col0, y=col1)
        plt.xlabel("Sequence ids")
        plt.ylabel("No. of samples")
        utils.saveFigure(out_fn)

    def plot_details(self, out_fn):
        if self._data_df.empty: return
        plt.figure()
        plt.tight_layout()
        self._data_df.sort_values(by=self._data_df.columns[0], ascending=True, inplace=True)
        col0 = self._data_df.columns[0]
        col1 = self._data_df.columns[1]
        sns.scatterplot(data=self._data_df, x=col0, y=col1)
        plt.xlabel("No. of samples")
        plt.ylabel("Prob. of finding the sequence")
        utils.saveFigure(out_fn)
