import numpy as np
import matplotlib.pyplot as plt
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils


class Diversity3dPlotter:

    def __init__(self, data_df, max_ens=None):
        self._data_df = data_df
        self._debug_key=DockerInterop.get_instance().get_debug_key()
        self._max_ens=max_ens

    def plot(self, out_fn):
        if self._data_df.empty: return
        df=self._data_df.sort_values('Panning path')
        plt.figure()
        ax = plt.axes(projection='3d')
        i=0
        for index, row in df.iterrows():
            xline = list(range(0, len(df.columns)-1))
            yline = [i]*len(xline)
            i += 1
            zline = row[1:]
            ax.plot3D(xline, yline, zline)
        ax.xaxis.set_ticks(np.arange(0, len(xline), 1))
        ax.yaxis.set_ticks(np.arange(0, len(df), 1))
        ax.set_xlabel('Round')
        ax.set_ylabel('Panning path')
        ax.set_zlabel('ENS', rotation = 90)
        if self._max_ens is not None:
            ax.set_zlim3d(0, self._max_ens)
        plt.legend(df.index, ncol=1, loc='upper left', prop={'size': 6})
        utils.saveFigure(out_fn)

