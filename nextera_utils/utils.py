import matplotlib.pyplot as plt
from nextera_utils.docker_interop import DockerInterop
import seaborn as sns

def saveFigure(out_fn=None):
    debug_key = DockerInterop.get_instance().get_debug_key()
    if debug_key is None:
        if out_fn is not None:
            plt.savefig(out_fn)
    else:
        plt.show()


# def plot_single_heatmap(df, summarize_fraction, out_fn, sns_cmap='rocket', title=None):
#     if df.empty: return
#     plt.figure()
#     if title is None:
#         if summarize_fraction:
#             title = "Sum of fractions"
#         else:
#             title = "Counts"
#     plt.tick_params(axis='both', labelsize=6)
#     df.sort_index(ascending=True, inplace=True)
#     sns.heatmap(df, xticklabels=True, yticklabels=True, cmap=sns_cmap, annot=False)
#     plt.title(title)
#     plt.tight_layout()
#     saveFigure(out_fn)