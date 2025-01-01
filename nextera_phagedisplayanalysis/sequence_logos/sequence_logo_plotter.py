import logomaker
from numpy import matrix
import nextera_utils.utils as utils
from nextera_utils.docker_interop import DockerInterop
import matplotlib.pyplot as plt


class SequenceLogoPlotter:

    def __init__(self, data_df, summarize_fraction):
        self._data_df = data_df
        self._summarize_fraction = summarize_fraction
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    # def plot(self, out_fn, title):
    #     col = self._data_df.iloc[:, 0]
    #     lst = col.values.tolist()
    #     selected_to_type='counts'
    #     matrix = logomaker.alignment_to_matrix(lst,to_type=selected_to_type)
    #     crp_logo = logomaker.Logo(matrix, shade_below=.5, fade_below=.5, font_name='Arial Rounded MT Bold',
    #                               color_scheme='dmslogo_funcgroup')
    #     crp_logo.ax.set_ylabel(selected_to_type)
    #     plt.title(title)
    #     utils.saveFigure(out_fn)

    def plot(self, out_fn, title):
        df = self._data_df.transpose()
        df.index = df.index.map(int)
        x = df.sum().sum()
        if x <= len(df):
            unit = 'frequencies'
        else:
            unit = 'counts'
        crp_logo = logomaker.Logo(df, shade_below=.5, fade_below=.5, font_name='Arial Rounded MT Bold',
                                  color_scheme='dmslogo_funcgroup')
        crp_logo.ax.set_ylabel('Sum of ' + unit)
        plt.title(title)
        utils.saveFigure(out_fn)