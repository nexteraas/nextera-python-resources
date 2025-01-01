import nextera_utils.heatmap_plotter as utils_heatmap_plotter
import matplotlib.pyplot as plt


class HeatmapPlotter(utils_heatmap_plotter.HeatmapPlotter):

    def __init__(self, df, title, sns_cmap, summarize_fractions, sequence=None):
        super(HeatmapPlotter, self).__init__(df, title, sns_cmap)
        self._summarize_fractions = summarize_fractions
        self._sequence = sequence

    def _get_character_for_index(self, index):
        df_index = list(self._df.index)
        out = df_index.index(self._sequence[index])
        return out

    def _pre_process(self):
        pass

    def _post_process(self):
        if self._summarize_fractions:
            bar='Frequency'
        else:
            bar='counts'
        self._ax.collections[0].colorbar.set_label(bar)
        if self._sequence is None: return
        counter = 0
        for c in self._sequence:
            i = self._get_character_for_index(counter)
            plt.text(counter + 0.5, i + 0.5, '★', color='gold', size=20, ha='center', va='center')
            counter += 1