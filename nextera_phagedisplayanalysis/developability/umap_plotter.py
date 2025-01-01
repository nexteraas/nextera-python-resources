import umap
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils
from matplotlib.lines import Line2D


class UmapPlotter():
    def __init__(self, df, groups_col, n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean',
                 alpha=0.6, point_size=8, legend_size=6, random_state=42):
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._df = df
        self._groups_col = groups_col
        self._alpha = alpha
        self._point_size = point_size
        self._legend_size = legend_size
        self._random_state = random_state
        self._reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=n_components,
                                  metric=metric, low_memory=True, random_state=self._random_state)

    def plot(self, out_fn):
        df = self._df.loc[:, self._df.columns != self._groups_col]
        scaled_df = StandardScaler().fit_transform(df)
        embedding = self._reducer.fit_transform(scaled_df)
        groups_df = self._df[self._groups_col]
        colors_map = self.create_colors(groups_df)
        colors = self.get_colors(groups_df, colors_map)
        fig, ax = plt.subplots()
        scatter = ax.scatter(embedding[:, 0], embedding[:, 1], c=colors, alpha=self._alpha, s=self._point_size)
        self.insert_legend(colors_map, ax)
        utils.saveFigure(out_fn)

    def create_colors(self, col):
        u=col.unique()
        out={}
        c = sns.color_palette(n_colors=len(u))
        for i in range(len(u)):
            out[u[i]]=c[i]
        return out

    def get_colors(self, col, colors):
        out=[]
        for x in col:
            col=colors.get(x)
            out.append(col)
        return out

    def insert_legend(self, colors_map, ax):
        if self._legend_size==0:
            return
        custom_lines = []
        custom_labels = []
        for key, value in colors_map.items():
            l = Line2D([0], [0], color=value, lw=4)
            custom_lines.append(l)
            custom_labels.append(key)
        ax.legend(custom_lines, custom_labels, prop={'size': self._legend_size})

