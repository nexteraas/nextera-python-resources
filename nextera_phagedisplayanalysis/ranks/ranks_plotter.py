import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse

from nextera_utils.docker_interop import DockerInterop


class RanksPlotter:

    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key=DockerInterop.get_instance().get_debug_key()

    def plot(self, out_fn):
        categories = []
        values = []
        labels = []
        rel_freq_categories = []
        no_of_pannings = (len(self._data_df.columns)/2)
        fig, ax = plt.subplots()
        plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='center', fontsize='x-small')
        plt.ylabel("Frequencies")
        self._extract_values(categories, values, labels, rel_freq_categories)
        for x in zip(categories, values, labels, rel_freq_categories):
            plt.plot(x[0], x[1], marker='o', label=x[2])
            # sns.lineplot(x[0], x[1], marker='o', label=x[2])
        plt.legend(loc="upper right")
        plt.xlim([0, no_of_pannings])
        self._add_relative_freqs_indications(no_of_pannings, categories, values, rel_freq_categories, ax)
        plt.tight_layout()
        if self._debug_key is None:
            plt.savefig(out_fn)
        else:
            plt.show()

    def _extract_values(self, categories, values, labels, rel_freq_categories):
        for index, row in self._data_df.iterrows():
            current_categories = []
            current_values = []
            current_rel_freq_categories = []
            labels.append(row.name)
            for i in range(0, len(self._data_df.columns), 2):
                col = self._data_df.columns[i]
                value = row[col]
                current_values.append(value)
                current_categories.append(col)
                rel_freq = row[self._data_df.columns[i+1]]
                if rel_freq > 0.9:
                    current_rel_freq_categories.append(1)
                elif rel_freq > 0.5:
                    current_rel_freq_categories.append(2)
                elif rel_freq > 0.1:
                    current_rel_freq_categories.append(3)
                else:
                    current_rel_freq_categories.append(4)
            categories.append(current_categories)
            values.append(current_values)
            rel_freq_categories.append(current_rel_freq_categories)

    def _add_relative_freqs_indications(self, no_of_pannings, categories, values, rel_freq_categories, ax):
        ell_height = ax.get_ylim()[1] / 10
        ell_width = no_of_pannings / 10
        for x in zip(categories, values, rel_freq_categories):
            for i in range(0, len(x[0])):
                if x[2][i] == 1:
                    circle1 = Ellipse([x[0][i], x[1][i]], width=ell_width, height=ell_height, color='black',
                                      fill=False, linestyle='-')
                    ax.add_patch(circle1)
                elif x[2][i] == 2:
                    circle1 = Ellipse([x[0][i], x[1][i]], width=ell_width, height=ell_height, color='black',
                                      fill=False, linestyle='dotted')
                    ax.add_patch(circle1)
