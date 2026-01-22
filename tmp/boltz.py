from numpy import load
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

def plot_npz_data(data):
    #uniform_data = np.random.rand(10, 12)
    ax = sns.heatmap(data)
    plt.show()


fn="C:/temp/boltz/raclone_pde.npz"
data = load(fn)
lst = data.files
for item in lst:
    print(item)
    plot_npz_data(data[item])