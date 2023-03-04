import math

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
import numpy as np
from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circle_heatmap import CircleHeatmap
import pandas as pd
import nextera_utils.utils as utils


class HeatmapPlotter(object):

    def __init__(self, df, title='', sns_cmap='rocket'):
        self._df = df
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._cmap=sns_cmap
        self._title=title
        self._ax=None

    def plot(self, out_fn):
        self._pre_process()
        if self._df.empty: return
        plt.figure()
        plt.tick_params(axis='both', labelsize=6)
        self._df.sort_index(ascending=True, inplace=True)
        self._ax = sns.heatmap(self._df, xticklabels=True, yticklabels=True, cmap=self._cmap, annot=False)
        plt.tight_layout()
        plt.title(self._title)
        self._post_process()
        utils.saveFigure(out_fn)

    def _pre_process(self):
        pass

    def _post_process(self):
        pass