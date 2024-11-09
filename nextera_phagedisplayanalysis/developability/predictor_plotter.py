from networkx.algorithms.bipartite import color
from setuptools.msvc import winreg

from nextera_utils.docker_interop import DockerInterop
import nextera_utils.utils as utils
from deep_sp.deep_sp import DeepSP, Quartiles
import copy
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle


class CompositeRectangle(object):
    def __init__(self, xy, width, height, color_top=None, color_left=None, color_right=None):
        self._rectangles=[]
        if (color_top is not None) and (color_left is not None) and (color_right is not None):
            self._create_three_color_composite(xy, width, height, color_top, color_left, color_right)
        elif (color_left is not None) and (color_right is not None):
            self._create_two_color_composite(xy, width, height, color_left, color_right)
        elif (color_top is not None) :
            self._create_one_color_composite(xy, width, height, color_top)
        else:
            raise NotImplementedError()

    def _create_three_color_composite(self, xy, width, height, color_top, color_left, color_right):
        x1 = xy[0]
        y1 = xy[1]
        y1 = y1 + height*0.66
        x1y1 = (x1, y1)
        height1 = height * 0.33
        rect = self._create_rectangle(x1y1, width, height1, color_top)
        self._rectangles.append(rect)
        height23=height*0.66
        self._create_two_color_composite(xy, width, height23, color_left, color_right)

    def _create_two_color_composite(self, xy, width, height, color_left, color_right):
        width = width/2
        rect = self._create_rectangle(xy, width, height, color_left)
        self._rectangles.append(rect)
        x2 = xy[0] + width
        y2 = xy[1]
        x2y2=(x2, y2)
        rect = self._create_rectangle(x2y2, width, height, color_right)
        self._rectangles.append(rect)

    def _create_one_color_composite(self, xy, width, height, color):
        rect = self._create_rectangle(xy, width, height, color)
        self._rectangles.append(rect)

    def _create_rectangle(self, xy, width, height, color):
        out = plt.Rectangle(xy=xy, width=width, height=height, color=color)
        return out

    def plot(self, ax):
        for r in self._rectangles:
            ax.add_patch(r)


class AirPlotter(object):
    def __init__(self, df):
        self._composites = {}
        self._names = []
        for r in range(0, len(df)):
            air = self._create(df, r)
            name = df.loc[r, 'Name']
            self._names.append(name)
            self._composites[name] = air

    def _create(self, df, r):
        air=[]
        c = self._get_color(df, r, 'CDR')
        rect = self._create_cdrs(c[0], c[1], c[2])
        air.append(rect)
        c = self._get_color(df, r, 'Fv')
        rect = self._create_fv(c[0], c[1], c[2])
        air.append(rect)
        c = self._get_color(df, r, 'Hv')
        rect = self._create_h_chain(c[0], c[1], c[2])
        air.append(rect)
        c = self._get_color(df, r, 'Lv')
        rect = self._create_l_chain(c[0], c[1], c[2])
        air.append(rect)
        c = self._get_color(df, r, 'CDRL1')
        rect = self._create_l_cdr(c[0], c[1], c[2], 1)
        air.append(rect)
        c = self._get_color(df, r, 'CDRL2')
        rect = self._create_l_cdr(c[0], c[1], c[2], 2)
        air.append(rect)
        c = self._get_color(df, r, 'CDRL3')
        rect = self._create_l_cdr(c[0], c[1], c[2], 3)
        air.append(rect)
        c = self._get_color(df, r, 'CDRH1')
        rect = self._create_h_cdr(c[0], c[1], c[2], 1)
        air.append(rect)
        c = self._get_color(df, r, 'CDRH2')
        rect = self._create_h_cdr(c[0], c[1], c[2], 2)
        air.append(rect)
        c = self._get_color(df, r, 'CDRH3')
        rect = self._create_h_cdr(c[0], c[1], c[2], 3)
        air.append(rect)
        return air

    def _get_color(self, df, row, region):
        s = 'SAP_pos_' + region
        c1 = self._get_color_value(df.loc[row, s], False)
        s = 'SCM_pos_' + region
        c2 = self._get_color_value(df.loc[row, s], True)
        s = 'SCM_neg_' + region
        c3 = self._get_color_value(df.loc[row, s], False)
        return c1, c2, c3

    def _get_color_value(self, value, highIsPositive):
        if highIsPositive:
            if value == 1:
                return 'r'
            elif value == 2:
                return 'y'
            elif value == 3:
                return 'b'
            elif value == 4:
                return 'g'
            else:
                raise NotImplementedError()
        else:
            if value==4:
                return 'r'
            elif value==3:
                return 'y'
            elif value==2:
                return 'b'
            elif value==1:
                return 'g'
            else:
                raise NotImplementedError()

    def _create_cdrs(self, color_top=None, color_left=None, color_right=None):
        xy = (0.1, 0.8)
        out = CompositeRectangle(xy, width=0.8, height=0.1, color_top=color_top, color_left=color_left, color_right=color_right)
        return out

    def _create_fv(self, color_top=None, color_left=None, color_right=None):
        xy = (0.45, 0.1)
        out = CompositeRectangle(xy, width=0.1, height=0.6, color_top=color_top, color_left=color_left, color_right=color_right)
        return out

    def _create_l_chain(self, color_top=None, color_left=None, color_right=None):
        xy = (0.30, 0.1)
        out = CompositeRectangle(xy, width=0.1, height=0.6, color_top=color_top, color_left=color_left, color_right=color_right)
        return out

    def _create_h_chain(self, color_top=None, color_left=None, color_right=None):
        xy = (0.60, 0.1)
        out = CompositeRectangle(xy, width=0.1, height=0.6, color_top=color_top, color_left=color_left, color_right=color_right)
        return out

    def _create_l_cdr(self, color_top=None, color_left=None, color_right=None, cdr_no=None):
        x = (cdr_no-1) * 0.15
        xy = (0.15, 0.3 + x)
        out = CompositeRectangle(xy, width=0.1, height=0.1, color_top=color_top, color_left=color_left,
                                 color_right=color_right)
        return out

    def _create_h_cdr(self, color_top=None, color_left=None, color_right=None, cdr_no=None):
        x = (cdr_no - 1) * 0.15
        xy = (0.75, 0.3 + x)
        out = CompositeRectangle(xy, width=0.1, height=0.1, color_top=color_top, color_left=color_left,
                                 color_right=color_right)
        return out

    def plot(self):
        fig, axs = plt.subplots(4, 6)
        sorted_names=sorted(self._names)
        i = 0
        for a1 in axs:
            for a2 in a1:
                a2.set_xticks([])
                a2.set_yticks([])
        for a1 in axs:
            for a2 in a1:
                ax = a2
                if i < len(sorted_names):
                    name = sorted_names[i]
                    air = self._composites[name]
                    i += 1
                    for c in air:
                        c.plot(ax)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    ax.set_title(name, fontsize=8, pad=0)


class PredictorPlotter(object):
    def __init__(self, data_df):
        self._data_df = data_df
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._developability_df = None
        self._quartiles_df = None

    def calculate_developability(self):
        if self._data_df.empty: return
        predictor = DeepSP()
        self._developability_df = predictor.run(self._data_df)
        return self._developability_df

    def get_developability_df(self):
        return self._developability_df

    def plot_data(self, out_fn=None):
        if self._developability_df is None or self._developability_df.empty: return
        if self._debug_key is None:
            if out_fn is not None:
                self._developability_df.to_csv(out_fn, index=False, sep ='\t')
        else:
            print(self._developability_df)

    def plot_quartiles(self, out_fn=None):
        if self._developability_df is None or self._developability_df.empty: return
        self._quartiles_df = copy.deepcopy(self._developability_df)
        quartiles =  Quartiles()
        for index in range(0, len(self._developability_df)):
            for column in self._developability_df:
                if column != 'Name':
                    val=self._developability_df.loc[index, column]
                    property=column.replace('_', '')
                    q=quartiles.get_quartile(property, val)
                    self._quartiles_df.loc[index, column] = q
        if self._debug_key is None:
            if out_fn is not None:
                #print('self._quartiles_df:')
                #print(self._quartiles_df)
                self._quartiles_df.to_csv(out_fn, index=False, sep ='\t')
        else:
            print(self._quartiles_df)

    def plot_air_representations(self, out_fn):
        air_plotter = AirPlotter(self._quartiles_df)
        air_plotter.plot()
        utils.saveFigure(out_fn)

#
# df = pd.DataFrame.from_dict({'SAP_CDRS': [4, 2, 1, 3], 'SCM_pos_CDRS': [2,2,1,3], 'SCM_neg_CDRS': [2,2,3,1],
#                             'SAP_Fv': [4, 2, 1, 3], 'SCM_pos_Fv': [2,2,1,3], 'SCM_neg_Fv': [2,2,3,1],
#                              'SAP_L_chain': [4, 2, 1, 3], 'SCM_pos_L_chain': [2,2,1,3], 'SCM_neg_L_chain': [2,2,3,1],
#                              'SAP_H_chain': [4, 2, 1, 3], 'SCM_pos_H_chain': [2,2,1,3], 'SCM_neg_H_chain': [2,2,3,1],
#                              'SAP_L_CDR1': [4, 2, 1, 3], 'SCM_pos_L_CDR1': [2,2,1,3], 'SCM_neg_L_CDR1': [2,2,3,1],
#                              'SAP_L_CDR2': [4, 2, 1, 3], 'SCM_pos_L_CDR2': [2,2,1,3], 'SCM_neg_L_CDR2': [2,2,3,1],
#                              'SAP_L_CDR3': [4, 2, 1, 3], 'SCM_pos_L_CDR3': [2,2,1,3], 'SCM_neg_L_CDR3': [2,2,3,1],
#                              'SAP_H_CDR1': [4, 2, 1, 3], 'SCM_pos_H_CDR1': [2,2,1,3], 'SCM_neg_H_CDR1': [2,2,3,1],
#                              'SAP_H_CDR2': [4, 2, 1, 3], 'SCM_pos_H_CDR2': [2,2,1,3], 'SCM_neg_H_CDR2': [2,2,3,1],
#                              'SAP_H_CDR3': [4, 2, 1, 3], 'SCM_pos_H_CDR3': [2,2,1,3], 'SCM_neg_H_CDR3': [2,2,3,1]
#                              })
# ap=AirPlotter(df)
# ap.plot()
# plt.show()
