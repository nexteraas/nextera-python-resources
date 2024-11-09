import umap
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils


class UmapPlotter():
    def __init__(self, data_df, groups_df, random_state=42):
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._data_df = data_df
        self._groups_df = groups_df
        self._random_state = random_state

    def plot(self, out_fn):
        reducer = umap.UMAP(random_state=self._random_state)
        scaled_df = StandardScaler().fit_transform(self._data_df)
        embedding = reducer.fit_transform(scaled_df)
        plt.scatter(embedding[:, 0], embedding[:, 1],c=[sns.color_palette()[x] for x in self._group_df[0].map({"Adelie":0, "Chinstrap":1, "Gentoo":2})])
        plt.gca().set_aspect('equal', 'datalim')
        plt.title('UMAP projection')
        if self._developability_df is None or self._developability_df.empty: return
        utils.saveFigure(out_fn)