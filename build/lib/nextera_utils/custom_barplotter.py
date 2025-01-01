from builtins import object
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

class CustomBarplotter(object):

    def __init__(self):
        pass

    def plot(self,  f_name):
        # Columns: ID	Binding	Samples
        df = pd.read_csv(f_name, sep='\t', index_col=0)
        df = df.sort_values('Samples', ascending=False)
        fig, ax = plt.subplots()
        height = df['Samples']
        #height = np.log10(df['Samples'])
        bars = list(df.index.str.slice(0,5)+'...')
        cmap = mpl.cm.get_cmap('Spectral_r')
        max=df['Binding'].max()
        color_intensities=df['Binding']/max
        colors=cmap(color_intensities)
        plt.bar(bars, height, color=colors)
        plt.xticks(rotation=90)
        sm = plt.cm.ScalarMappable(cmap=cmap)
        sm.set_clim(vmin=0, vmax=max)
        cbar = plt.colorbar(sm)
        cbar.set_label('Binding ratio')
        plt.ylabel("No. of colonies")
        fig.subplots_adjust(bottom=0.2)
        plt.yscale('log')
        plt.title('PRAME binders (a=0.99)')
        plt.show()

plotter=CustomBarplotter()

plotter.plot("C:/Nextera/analysis/wetlab_binding_data/input_prame.txt")
#
# # libraries
# import numpy as np
# import matplotlib.pyplot as plt
#
# # create a dataset
# height = [3, 12, 5, 18, 45]
# bars = ('A', 'B', 'C', 'D', 'E')
# x_pos = np.arange(len(bars))
#
# # Create bars with different colors
# plt.bar(x_pos, height, color=['black', 'red', 'green', 'blue', 'cyan'])
#
# # Create names on the x-axis
# plt.xticks(x_pos, bars)
#
# # Show graph
# plt.show()