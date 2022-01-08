import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from resources.docker_interop import DockerInterop
from matplotlib.ticker import MaxNLocator

di=DockerInterop()
args=di.get_args()
in_fn=args['in_fn']
swi_out_fn=args['swi_out_fn']
ens_out_fn=args['ens_out_fn']

def load_data(df):
    series_names=df['Series'].unique()
    out=[]
    for serie in series_names:
        tmp_df= df[df['Series'] == serie]
        out.append(tmp_df)
    return out

def plot(dfs, idx, out_fn):
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # name = "Accent"
    # cmap = plt.get_cmap(name)  # type: matplotlib.colors.ListedColormap
    # colors = cmap.colors  # type: list
    current_group = None
    previous_group = None
    z = 0
    for df in dfs:
        current_group = df['Group'].iloc[0]
        current_series = df['Series'].iloc[0]
        if previous_group is None:
            previous_group = current_group
        if current_group == previous_group:
            z += 0.5
        else:
            current_group = df['Group'].iloc[0]
            z += 1
        z_tmp = np.linspace(z, z, num=df.shape[0])
        x = np.linspace(0, df.shape[0]-1, num=df.shape[0])
        y = df[idx]
        # ax.set_prop_cycle(color=colors)
        lbl = current_series + " (" + current_group + ")"
        ax.plot(x, z_tmp, y, label=lbl, marker='o')
        previous_group = current_group
    ax.set_xlabel('Rounds')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel('Sample')
    ax.set_zlabel(idx)
    ax.legend(loc='upper left', bbox_to_anchor=(-0.2, 1.15), prop={'size': 6}, ncol=4)
    fig.savefig(out_fn)
    #plt.show()

df=di.read_df(di.get_input_fn(in_fn))
dfs=load_data(df)
out_fn=di.get_output_fn(swi_out_fn)
plot(dfs, 'SWI', out_fn)
out_fn=di.get_output_fn(ens_out_fn)
plot(dfs, 'ENS', out_fn)
