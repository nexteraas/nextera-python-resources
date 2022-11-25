import matplotlib.pyplot as plt
import numpy as np
from nextera_utils.docker_interop import DockerInterop
import seaborn as sns
import enum
import nextera_utils.utils as utils


class Mode(enum.Enum):
    cdr3_length = 1
    gene_usage = 2


class BarchartPlotter:
    _CDR_LENGTH_HEADER = 'CDR3 length'
    _GENE_USAGE_HEADER = 'V'
    _PANNING_HEADER = 'Panning'

    def __init__(self, data_df, summarize_fraction, mode):
        self._data_df = data_df
        self._summarize_fraction = summarize_fraction
        self._mode=mode
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    def plot(self, out_fn):
        if self._data_df.empty: return
        fig = plt.figure()
        values_header=list(self._data_df.columns)[-1]
        col_header=self._get_col_header()
        df = self._data_df.pivot_table(values_header, index=BarchartPlotter._PANNING_HEADER, columns=col_header)
        df.fillna(0.0, inplace=True)
        df = df.reindex(sorted(df.columns), axis=1)
        length_range = np.arange(df.shape[1])
        row_no = df.shape[0]
        width = 0.8 / row_no
        #offset = -width / 2
        offset = -0.4
        palette = sns.color_palette('hls', n_colors=row_no)
        i = 0
        for index, row in df.iterrows():
            plt.bar(length_range + offset, row, width, color=palette[i])
            offset += width
            i += 1
        plt.xticks(length_range, list(df.columns.values), fontsize=8)
        plt.xlabel(self._get_xlabel())
        plt.ylabel(self._get_ylabel())
        if self._mode==Mode.gene_usage:
            plt.xticks(rotation=90)
        plt.legend(list(df.index.values))
        plt.tight_layout()
        utils.saveFigure(out_fn)

    def _get_col_header(self):
        if self._mode==Mode.cdr3_length:
            return BarchartPlotter._CDR_LENGTH_HEADER
        elif self._mode == Mode.gene_usage:
            return BarchartPlotter._GENE_USAGE_HEADER

    def _get_xlabel(self):
        if self._mode==Mode.cdr3_length:
            return 'CDR3 length'
        elif self._mode == Mode.gene_usage:
            return 'Gene'

    def _get_ylabel(self):
        if self._summarize_fraction:
            return 'Frequencies'
        else:
            return 'Counts'
