from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
import nextera_utils.utils as utils
from nextera_utils.docker_interop import DockerInterop
from nextera_utils.circos_venn import CircosVenn
from nextera_utils.circos_venn import Set
from nextera_utils.circos_venn import Sets
from nextera_utils.circos_venn import Intersection
from nextera_utils.circos_venn import Intersections
from nextera_utils.circos_venn import InputData


class SequenceOverlapPlotter():

    def __init__(self, data_df, plot_curves, crossing_intersections):
        self._data_df = data_df
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._plot_curves = plot_curves
        self._crossing_intersections = crossing_intersections

    def plot(self, out_fn):
        if self._data_df.empty: return
        sets_df =self._data_df[self._data_df['Intersection'] == 0]
        intersections_df = self._data_df[self._data_df['Intersection'] == 1]
        sorted_sets_df = sets_df.sort_values('Sort order')
        set_list=[]
        for index, row in sorted_sets_df.iterrows():
            size = int(row['Shared seqs.'])
            set = Set(row['Pannings'], size)
            if set.get_size()>0:
                set_list.append(set)
        sets = Sets(set_list)
        intersection_list=[]
        for index, row in intersections_df.iterrows():
            isect_sets = self._get_intersection_sets(row['Pannings'], sets)
            size = int(row['Shared seqs.'])
            isect = Intersection(Sets(isect_sets), size, 0.3)
            if isect.get_size()>0:
                intersection_list.append(isect)
        intersections=Intersections(intersection_list)
        if sets.size()>0 and  intersections.size()>0:
            input_data = InputData(sets, intersections)
            input_data.scale(sets, intersections, to_sum_of_sizes=500, min_sum_of_sizes=48)
            cv = CircosVenn(input_data, crossing_intersections=self._crossing_intersections,
                            curves=self._plot_curves, off_center=0.8)
            plt.figure()
            cv.plot()
            utils.saveFigure(out_fn)

    def _get_intersection_sets(self, intersection_text, sets):
        out=[]
        for set in sets:
            if self._intersection_text_contains_set(intersection_text, set):
                out.append(set)
        return out

    def _intersection_text_contains_set(self, intersection_text, set):
        i = intersection_text.find(set.get_label())
        if i==-1:
            return False
        if i + len(set.get_label())==len(intersection_text):
            return True
        i = i + len(set.get_label())
        if intersection_text[i : i+2]==', ':
            return True
        return False
