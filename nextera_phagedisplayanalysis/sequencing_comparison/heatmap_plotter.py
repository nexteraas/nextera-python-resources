import math

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
import numpy as np
from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circle_heatmap import CircleHeatmap
import pandas as pd


class HeatmapPlotter():

    def __init__(self, data_df, summarize_fraction):
        self._data_df = data_df
        self._summarize_fraction = summarize_fraction
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    def plot_single_heatmap(self, out_fn):
        plt.figure()
        if self._summarize_fraction:
            title = "Sum [Fraction]"
        else:
            title = "Count [Fraction]"
        plt.tick_params(axis='both', labelsize=6)
        df=self._data_df.transpose()
        df = df.reindex(sorted(df.columns), axis=1)
        df.sort_index(ascending=True, inplace=True)
        sns.heatmap(df, xticklabels=True, yticklabels=True, cmap='rocket', annot=False)
        plt.title(title)
        plt.tight_layout()
        if self._debug_key is None:
            plt.savefig(out_fn)
        else:
            plt.show()

    def plot_difference_heatmaps(self, out_fn):
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
        if self._summarize_fraction:
            value_col_a = "Sum [Fraction](1) - Sum [Fraction](2)"
            value_col_b = "Sum [Fraction](1) / Sum [Fraction](2)"
        else:
            value_col_a = "Count [Fraction](1) - Count [Fraction](2)"
            value_col_b = "Count [Fraction](1) / Count [Fraction](2)"
        self._create_heatmap_subtraction(value_col_a, "Item 1 - Item 2", axes[0])
        self._create_heatmap_division(value_col_b, "Item 1 / Item 2", axes[1])
        axes[0].tick_params(axis='both', labelsize=5)
        axes[1].tick_params(axis='both', labelsize=5)
        plt.tight_layout()
        if self._debug_key is None:
            plt.savefig(out_fn)
        else:
            plt.show()

    def _create_heatmap_subtraction(self, value_col, title, axis):
        df = self._data_df.copy()
        df.reset_index(inplace=True)
        v_min = self._data_df[value_col].min()
        v_max = self._data_df[value_col].max()
        if abs(v_min)>abs(v_max):
            v=abs(v_min)
        else:
            v = abs(v_max)
        axis.set_title(title)
        df1=pd.pivot_table(df, values=value_col, index='chain1-V', columns='chain2-V')
        df1=df1.transpose()
        df1.fillna(0.0, inplace=True)
        df1 = df1.reindex(sorted(df1.columns), axis=1)
        df1.sort_index(ascending=True, inplace=True)
        sns.heatmap(df1, xticklabels=True, yticklabels=True, ax=axis, cmap='icefire',
                    center=0.0, vmin=-1*v, vmax=v, annot=False)

    def _create_heatmap_division(self, value_col, title, axis):
        df = self._data_df.copy()
        df.reset_index(inplace=True)
        axis.set_title(title)
        max = self._get_non_inf_max_value(df, value_col)
        df[value_col] = np.where(float("inf") == df[value_col], max, df[value_col])
        df[value_col] = np.where(df[value_col] > 1,  1+(df[value_col]/max), df[value_col])
        df1=pd.pivot_table(df, values=value_col, index='chain1-V', columns='chain2-V')
        df1 = df1.transpose()
        df1.fillna(0.0, inplace=True)
        df1 = df1.reindex(sorted(df1.columns), axis=1)
        df1.sort_index(ascending=True, inplace=True)
        sns.heatmap(df1, xticklabels=True, yticklabels=True, ax=axis, cmap='icefire',
                    center=1, vmin=0, vmax=2, annot=False)

    def _get_non_inf_max_value(self, df, col):
        out=float('-inf')
        for row in df[col]:
            x = row
            if float("inf") != x:
                if (x > out):
                    out = x
        return out
