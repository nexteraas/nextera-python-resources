import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
import numpy as np
import enum
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils


class HistogramPlotter:

    def __init__(self, data_df, summarize_fraction, mode):
        self._data_df = data_df
        self._summarize_fraction = summarize_fraction
        self._mode = mode
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    def plot(self, out_fn):
        if self._data_df.empty: return
        data1 = self._data_df.iloc[:,0]
        data2 = self._data_df.iloc[:, 1]
        keys1 = list(data1.keys())
        keys2 = list(data2.keys())
        fig = plt.figure()
        plt.bar(keys1, list(data1), color='red', alpha=0.4, width=0.8)
        plt.bar(keys2, list(data2), color='blue', alpha=0.4, width=0.8)
        plt.legend(['Pair item 1','Pair item 2'])
        plt.title("Sequencing comparison")
        if self._summarize_fraction:
            plt.ylabel("Fraction")
        else:
            plt.ylabel("Count")
        if self._mode==Mode.Cdr3Usage:
            plt.xlabel("CDR3 length")
        elif self._mode == Mode.NInserts:
            plt.xlabel("N inserts")
        elif self._mode==Mode.GeneUsage:
            plt.xlabel("V gene")
            plt.xticks(fontsize=8, rotation=90)
        plt.tight_layout()
        utils.saveFigure(out_fn)


class Mode(enum.Enum):
    Cdr3Usage = 1
    GeneUsage = 2