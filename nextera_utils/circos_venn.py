from math import cos
from math import sin
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy import interpolate
from matplotlib.lines import Line2D
import math
from distinctipy import get_colors


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Set(object):
    def __init__(self, label, size, color=None):
        self._label = label
        self._size = size
        self._points = []
        self._point_index = -1
        self._proportion = 0
        self._color = color

    def get_color(self):
        return self._color

    def get_label(self):
        return self._label

    def get_point_index(self):
        return self._point_index

    def get_indexed_point(self):
        out = self._points[self._point_index]
        return out

    def set_point_index(self, index):
        self._point_index = index

    def add_to_point_index(self, value):
        self._point_index += value

    def append_point(self, point):
        self._points.append(point)

    def get_points(self):
        return self._points

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size


class Sets(object):
    def __init__(self, sets_list=[]):
        self._items=sets_list
        self._set_colors()

    def __iter__(self):
        self._iter_n = 0
        return self

    def __next__(self):
        if self._iter_n < len(self._items):
            result = self._items[self._iter_n]
            self._iter_n += 1
            return result
        else:
            raise StopIteration

    def _set_colors(self):
        color_n = 0
        for set in self._items:
            if set._color is None:
                color_n += 1
        colors = get_colors(color_n)
        index = 0
        for set in self._items:
            if set._color is None:
                set._color = colors[index]
                index += 1

    def add(self, set):
        self._items.append(set)
        self._calculate_proportions()

    def get(self, index):
        return self._items[index]

    def get_by_label(self, label):
        for set in self._items:
            if set.get_label() == label:
                return set
        return None

    def _calculate_proportions(self):
        total = self.get_sum_of_sizes()
        for set in self._items:
            set._proportion = set._size / total

    def get_sum_of_sizes(self):
        total = 0
        for set in self._items:
            total += set._size
        return total

    def set_point_indices(self, index):
        for set in self._items:
            set._point_index=index

    def size(self):
        return len(self._items)


class Intersection(object):
    def __init__(self, sets, size, alpha=None):
        self._sets = sets
        self._size = size
        self._alpha = alpha

    def get_sets(self):
        return self._sets

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def get_pairs(self):
        out = []
        for i in range(0, self._sets.size()-1):
            for j in range(i+1, self._sets.size()):
                s1 = self._sets._items[i]
                s2 = self._sets._items[j]
                pair = [s1, s2]
                out.append(pair)
        return out

    def get_avg_color(self):
        r = []
        g = []
        b = []
        for set in self._sets:
            c_r, c_g, c_b, c_a = colors.to_rgba(set._color)
            r.append(c_r)
            g.append(c_g)
            b.append(c_b)
        r = sum(r)
        g = sum(g)
        b = sum(b)
        s = self._sets.size()
        out = r / s, g / s, b / s, self._alpha
        return out


class Intersections(object):
    def __init__(self, intersections=[]):
        self._items = intersections
        self.calculate_alphas()
        self.validate()

    def __iter__(self):
        self._iter_n = 0
        return self

    def __next__(self):
        if self._iter_n < len(self._items):
            result = self._items[self._iter_n]
            self._iter_n += 1
            return result
        else:
            raise StopIteration

    def validate(self):
        sets_map = {}
        for isect in self._items:
            for set in isect.get_sets():
                sets_map[set] = set
        set_list = []
        for set_key, set in sets_map.items():
            set_list.append(set)
        sets = Sets(set_list)
        for set in sets:
            set_isect_count = self._get_intersection_counts(set)
            if set_isect_count>set.get_size():
                raise ValueError('Set size smaller then defined intersections')

    def decrease_interaction_size(self):
        sorted_items = sorted(self._items, key=lambda x: x._size, reverse=True)
        value = sorted_items[0].get_size()-1
        sorted_items[0].set_size(value)

    def _get_intersection_counts(self, set):
        out = 0
        for isect in self._items:
            isect_set = isect.get_sets().get_by_label(set.get_label())
            if not isect_set is None:
                out += isect.get_size()
        return out

    def calculate_alphas(self, override=False):
        total = 0
        for isec in self._items:
            total += isec.get_size() * isec.get_sets().size()
        if total == 0:
            a = 0.75
        else:
            a = (total ** -0.9) * 20
        # if a > 1:
        #     a = 1
        if a > 0.75:
            a = 0.75
        for isec in self._items:
            if (isec._alpha is None) or override:
                isec._alpha = a

    def size(self):
        return len(self._items)


class LineCache(object):
    def __init__(self, off_center=0.7):
        self._items = []
        self._off_center = off_center

    def add(self, point1, point2, color):
        self._items.append([point1, point2, color])

    def plot(self, reverse=False, center=None):
        if reverse:
            for i in range(0, len(self._items)):
                point1 = self._items[i][0]
                index = len(self._items)-1-i
                point2 = self._items[index][1]
                self._plot_line(point1, point2, self._items[i][2], center)
        else:
            for line in self._items:
                self._plot_line(line[0], line[1], line[2], center)

    def _plot_line(self, p1, p2, color, center=None):
        if center is None:
            plt.plot([p1.x, p2.x], [p1.y, p2.y], color=color)
        else:
            x_m_point = (p1.x + p2.x) / 2
            y_m_point = (p1.y + p2.y) / 2
            x_m_point2 = (x_m_point + center.x) * self._off_center
            y_m_point2 = (y_m_point + center.y) * self._off_center
            nodes = np.array([[p1.x,p1.y], [x_m_point2, y_m_point2], [p2.x,p2.y]])
            x = nodes[:, 0]
            y = nodes[:, 1]
            tck, u = interpolate.splprep( [x,y] , k=2 )
            xnew, ynew = interpolate.splev(np.linspace(0, 1, 100), tck, der=0)
            plt.plot( xnew, ynew, color=color)


class InputData(object):
    def __init__(self, sets, intersections):
        self._sets = sets
        self._intersections = intersections
        self._original_n=self._create_original_n()

    def _create_original_n(self):
        out={}
        for set in self._sets:
            out[set]=set.get_size()
        return out

    def get_sets(self):
        return self._sets

    def get_intersections(self):
        return self._intersections

    def get_original_n(self, set):
        return self._original_n[set]

    def scale(self, sets, intersections, to_sum_of_sizes=500, min_sum_of_sizes=100):
        total = sets.get_sum_of_sizes()
        if total < min_sum_of_sizes:
            return sets, intersections
        scaling_factor = to_sum_of_sizes / total
        for set in sets:
            i = round(set.get_size() * scaling_factor, 0)
            set.set_size(int(i))
        for isect in intersections:
            i = round(isect.get_size() * scaling_factor, 0)
            isect.set_size(int(i))
        b = True
        while b:
            try:
                intersections.validate()
                b = False
            except:
                intersections.decrease_interaction_size()
        intersections.calculate_alphas(override=False)
        self._sets = sets
        self._intersections = intersections


class CircosVenn(object):
    def __init__(self, input_data, set_marker_size=None, crossing_intersections=True, curves=True, off_center=0.5):
        self._input_data = input_data
        self._assign_points()
        self._crossing_intersections = crossing_intersections
        self._curves = curves
        self._off_center = off_center
        if set_marker_size is None:
            if input_data.get_sets().get_sum_of_sizes()<48:
                self._set_marker_size = 5
            elif input_data.get_sets().get_sum_of_sizes()<150:
                self._set_marker_size = 3
            else:
                self._set_marker_size = 1
        else:
            self._set_marker_size = set_marker_size

    def _assign_points(self):
        step = (2 * math.pi) / self._input_data.get_sets().get_sum_of_sizes()
        counter = 0
        index = 0
        current_set = self._input_data.get_sets().get(index)
        for i in np.arange(0, 2 * math.pi, step):
            x = sin(i) * 1
            y = cos(i) * 1
            d = Point(x, y)
            current_set.append_point(d)
            counter += 1
            if counter == current_set.get_size():
                index += 1
                if index == self._input_data.get_sets().size(): break
                counter = 0
                current_set = self._input_data.get_sets().get(index)

    def plot(self):
        plt.xlim([-1.1,  1.1])
        plt.ylim([-1.1, 1.1])
        plt.gca().set_aspect('equal', 'datalim')
        legends = []
        labels = []
        for set in self._input_data.get_sets():
            l = True
            for point in set.get_points():
                if l:
                    label = set.get_label() + ' (n=' + str(self._input_data.get_original_n(set)) + ')'
                    l = False
                    h1 = Line2D([0], [0], marker='o', markersize=np.sqrt(20), color=set.get_color(), linestyle='None', label=label)
                    legends.append(h1)
                    labels.append(label)
                plt.plot(point.x, point.y, 'o', color=set._color, markersize=self._set_marker_size)
        self._plot_intersections()
        plt.legend(legends,labels, loc="upper right", markerscale=1, scatterpoints=1, fontsize=5)
        plt.axis('off')

    def _plot_intersections(self):
        self._input_data.get_sets().set_point_indices(0)
        for isec in self._input_data.get_intersections():
            pairs = isec.get_pairs()
            current_indices={}
            for set in isec.get_sets():
                current_indices[set] = set.get_point_index()
            c = isec.get_avg_color()
            for pair in pairs:
                lc = LineCache(off_center=self._off_center)
                pair[0].set_point_index(current_indices[pair[0]])
                pair[1].set_point_index(current_indices[pair[1]])
                for lines in range(0, isec._size):
                    from_point = pair[0].get_indexed_point()
                    to_point = pair[1].get_indexed_point()
                    lc.add(from_point, to_point, c)
                    pair[0].add_to_point_index(1)
                    pair[1].add_to_point_index(1)
                center = None
                if self._curves:
                    center = Point(0, 0)
                lc.plot(reverse=not (self._crossing_intersections), center=center)
            for set in isec._sets._items:
                set.set_point_index(current_indices[set]+isec.get_size())

