from builtins import object
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

class CustomScatterplotter(object):

    def __init__(self):
        pass

    def plot(self,  f_name, tag):
        # Columns: ID	Binding	Samples
        df = pd.read_csv(f_name, sep='\t', index_col=0)
        df = df.sort_values('CloneFreq', ascending=False)

        fig, ax = plt.subplots()
        plt.xscale('log')
        plt.yscale('log')


        cmap = mpl.cm.get_cmap('Spectral_r')
        max = df['Binding'].max()
        color_intensities = df['Binding'] / max

        colors = cmap(color_intensities)

        sm = plt.cm.ScalarMappable(cmap=cmap)
        sm.set_clim(vmin=0, vmax=max)
        cbar = plt.colorbar(sm)
        cbar.set_label('Binding ratio')

        #plt.xlabel("Specific target binding \n(ratio relevant/irrelevant target)")
        plt.xlabel("Specific target binding \n(EC50)")
        plt.ylabel("Clone frequency \n(% of total unique sequences)")
        plt.scatter(df['Binding'], df['CloneFreq'], color=colors, s=26)#, edgecolors='black')

        if tag=='Prame':
            n = ['Clone B', 'Clone A', '', '', '', 'Clone C', '', '', '']
            for i, txt in enumerate(n):
                ax.annotate(txt, (df['Binding'].iloc[i], df['CloneFreq'].iloc[i]))
            ax.set_xlim(10000000,1000000000)
        elif tag=='Mage':
            n = ['Clone A', '', 'Clone B', '', '', 'Clone C', '', '', '', '', '', '', 'Clone D', 'Clone E', '']
            for i, txt in enumerate(n):
                ax.annotate(txt, (df['Binding'].iloc[i], df['CloneFreq'].iloc[i]))
            ax.set_xlim(1, 100)
        fig.tight_layout()
        plt.show()

plotter=CustomScatterplotter()

plotter.plot("C:/Nextera/analysis/wetlab_binding_data/scatterplot_prame_ec50.txt", 'Prame')
