import matplotlib.pyplot as plt
import umap
import umap.plot
import pandas as pd
from nextera_utils.docker_interop import DockerInterop
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


class UmapPlotter:

    def __init__(self, data_df, n_neighbors=15, min_dist=0.1, n_components=2, metric='euclidean'):
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._data_df = data_df
        if not self._data_df.empty:
            scaled_features = self._scale_df(data_df)
            # scaled_features = StandardScaler().fit_transform(data_df)
            self._data_df = pd.DataFrame(scaled_features, index=data_df.index, columns=data_df.columns)
            #self._data_df = self._data_df.head(1000)
            self._reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist,
                                      n_components=n_components, metric=metric, low_memory=True)
            self._mapper = self._reducer.fit(self._data_df)

    def _scale_df(self, df):
        std_cols=[]
        for col in df.columns:
            one_hot_col = df[col].isin([0, 1]).all()
            if not one_hot_col:
                std_cols.append(col)
        ct = ColumnTransformer([
            ('somename', StandardScaler(), std_cols)
        ], remainder='passthrough')
        out=ct.fit_transform(df)
        return out

    def plot(self, out_fn, draw_custom_umap=True, draw_circle_highlights=True, colors=None):
        if self._data_df.empty: return
        fig = None
        if draw_custom_umap:
            self._plot_custom_umap(self._reducer, self._data_df, colors, colors, draw_circle_highlights)
        else:
            ax = umap.plot.points(self._mapper)
            fig = ax.get_figure()
        if self._debug_key is None:
            if fig is None:
                plt.savefig(out_fn)
            else:
                fig.savefig(out_fn)
        else:
            plt.show()

    def _plot_custom_umap(self, reducer, df, colors, highlights, draw_circle_highlights):
        if self._data_df.empty: return
        fig=plt.figure()
        colors = self._create_colors(self._data_df, colors)
        embedding = reducer.transform(df)
        scatter=plt.scatter(embedding[:, 0], embedding[:, 1], c=colors, alpha=0.2, s=1)
        plt.gca().set_aspect('equal', 'datalim')
        if draw_circle_highlights:
            missing_highlights = self._do_draw_circle_highlights(highlights, df, embedding)
            if missing_highlights>0:
                plt.title('(' + str(missing_highlights) + ' highlights not found)', fontsize=8,  y=-0.01)
            # handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
            # ax_list = fig.axes
            # legend2 = ax_list[0].legend(handles, labels, loc="upper right", title="Sizes")

    def _do_draw_circle_highlights(self, colors, df, coords):
        found_seq_ids = 0
        unique_colors = self._get_unique_colors(colors)
        for unique_color in unique_colors:
            seq_ids = self._get_seq_ids_for_color(colors, unique_color)
            indices = self._get_seq_id_indices(seq_ids, df)
            found_seq_ids += len(indices)
            self._draw_circles(indices, coords, unique_color)
        return len(colors) - found_seq_ids

    def _create_colors(self, df, colors):
        out = []
        for seq_id in df.index:
            predef_color = self._get_predef_color(seq_id, colors)
            if predef_color is None:
                out.append('#000000')
            else:
                out.append(predef_color)
        return out

    def _get_predef_color(self, seq_id, predef_colors):
        row = predef_colors.loc[predef_colors['Sequence ids'] == seq_id]
        if len(row) == 0:
            return None
        else:
            out = row['Color'][0]
            return out

    def _get_seq_id_indices(self, seq_ids, df):
        out = []
        for seq_id in seq_ids:
            i = self._get_seq_id_index(seq_id, df)
            if i is not None:
                out.append(i)
        return out

    def _get_seq_id_index(self, seq_id, df):
        out = 0
        for id in df.index:
            if id == seq_id:
                return out
            out += 1
        return None

    def _draw_circles(self, seq_id_indices, coords, color):
        for seq_id_index in seq_id_indices:
            center = coords[seq_id_index]
            plt.scatter(center[0], center[1], s=1000, facecolors='none', edgecolors=color)

    def _get_unique_colors(self, colors):
        out = colors['Color'].unique()
        return out

    def _get_seq_ids_for_color(self, colors, color):
        row = colors.loc[colors['Color'] == color]
        out = []
        if len(row) > 0:
            seq_ids = row['Sequence ids']
            for seq_id in seq_ids:
                out.append(seq_id.strip())
        return out
