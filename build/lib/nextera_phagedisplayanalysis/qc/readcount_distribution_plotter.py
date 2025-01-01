from builtins import object
from nextera_utils.docker_interop import DockerInterop
import matplotlib.pyplot as plt
import nextera_utils.utils as utils


class ReadcountDistributionPlotter(object):
    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key = DockerInterop.get_instance().get_debug_key()

    def plot(self, out_fn):
        if self._data_df.empty: return
        font_size = 8
        df = self._data_df.sort_values('RC', ascending=False)
        plt.figure()
        x, y = self._create_points(df)
        x_value = len(x)
        singletons = self._get_singletons(df)
        if singletons>0:
            x.append(x_value)
            y.append(1)
            x_value += 2
            x.append(x_value)
            y.append(1)
            x_value += 2
            x.append(x_value)
            y.append(1)
        plt.plot(x, y, marker="o", markersize=2)
        custom_x_lim = int(x_value * 1.2)
        plt.xlim([0, custom_x_lim])
        plt.xticks(fontsize=font_size)
        plt.yticks(fontsize=font_size)
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        if singletons>0:
            singletons_text='  // (1 RC:  + ' +  str(singletons)+ ')'
            plt.text(x_value, 0.5, singletons_text, fontsize=font_size)
        plt.xlabel("n")
        plt.ylabel("RC")
        utils.saveFigure(out_fn)

    def _create_points(self, df):
        x=[]
        y=[]
        x_value = 0
        for index, row in df.iterrows():
            i = int(row['n'])
            j = row['RC']
            if j < 2:
                break
            for ns in range(0, i):
                x.append(x_value)
                y.append(j)
                x_value += 1
        return x, y

    def _get_singletons(self, df):
        row_df = df.loc[df['RC'] == 1]
        if(len(row_df)==0):
            return -1
        out = row_df['n'].iloc[0]
        return out
