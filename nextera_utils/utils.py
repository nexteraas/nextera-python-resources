import matplotlib.pyplot as plt
from nextera_utils.docker_interop import DockerInterop
import seaborn as sns

def saveFigure(out_fn):
    debug_key = DockerInterop.get_instance().get_debug_key()
    if debug_key is None:
        plt.savefig(out_fn)
    else:
        plt.show()


def plot_single_heatmap(df, summarize_fraction, out_fn):
    if df.empty: return
    plt.figure()
    if summarize_fraction:
        title = "Sum [Fraction]"
    else:
        title = "Count [Fraction]"
    plt.tick_params(axis='both', labelsize=6)
    df.sort_index(ascending=True, inplace=True)
    sns.heatmap(df, xticklabels=True, yticklabels=True, cmap='rocket', annot=False)
    plt.title(title)
    plt.tight_layout()
    saveFigure(out_fn)