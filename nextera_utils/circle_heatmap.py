import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import pandas as pd


class CircleHeatmap:
    def __init__(self, df, size_factor=1, cmap="RdYlGn"):
        self._cmap=cmap
        rows = df.shape[0]
        cols = df.shape[1]
        self._x, self._y = np.meshgrid(np.arange(cols), np.arange(rows))
        self._R = np.zeros([rows, cols])
        self._c = np.random.rand(rows, cols) - 0.5
        f = 0.5/self._get_max_value(df, 0)
        f = f*size_factor
        for r in range(0,rows):
            for c in range(0, cols):
                x=df.iat[r,c]
                v=x[0]*f
                if v>1:
                    print (v)
                self._R[r][c]=v
                self._c[r][c]=x[1]
        self._xlabels = list(df)
        self._ylabels = list(df.index)

    def _get_max_value(self, df, index):
        rows = df.shape[0]
        cols = df.shape[1]
        out=float('-inf')
        for r in range(0, rows):
            for c in range(0, cols):
                x = df.iat[r, c]
                if(x[index]>out):
                    out=x[index]
        return out

    def plot(self, ax):
        circles = [plt.Circle((j, i), radius=r) for r, j, i in zip(self._R.flat, self._x.flat, self._y.flat)]
        col = PatchCollection(circles, array=self._c.flatten(), cmap=self._cmap)
        ax.add_collection(col)
        rows, cols = self._R.shape
        ax.set(xticks=np.arange(cols), yticks=np.arange(rows),
               xticklabels=self._xlabels, yticklabels=self._ylabels)
        ax.set_xticks(np.arange(cols + 1) - 0.5, minor=True)
        ax.set_yticks(np.arange(rows + 1) - 0.5, minor=True)
        ax.grid(which='minor')

#
# tmp={}
# tmp['a']=[[5,0], [10,0], [2,0], [5,0], [6,0]]
# tmp['b']=[[10,14], [3,0], [4,0], [2,0], [3,5]]
# tmp['c']=[[10,-20], [3,0], [4,0], [2,0], [3,0]]
# tmp['i']=['x', 'y', 'z', 'y2', 'z1']
# df=pd.DataFrame(tmp)
# df.set_index('i', inplace=True)
#
#
# ch=CircleHeatmap(df)
# ch.plot()
#
# exit()
#
#
# N = 10 # rows
# M = 11 #cols
# ylabels = ["".join(np.random.choice(list("PQRSTUVXYZ"), size=7)) for _ in range(N)] #rows
# xlabels = ["".join(np.random.choice(list("ABCDE"), size=3)) for _ in range(M)] #cols
#
# x, y = np.meshgrid(np.arange(M), np.arange(N))
# s = np.random.randint(0, 180, size=(N,M))
# c = np.random.rand(N, M)-0.5
#
# fig, ax = plt.subplots()
#
# R = s/s.max()/2
# count=.01
# R = np.zeros([N, M])
# for i in range(0, N):
#     for j in range(0, M):
#         R[i][j]=count
#         count+=.01
#
# circles = [plt.Circle((j,i), radius=r) for r, j, i in zip(R.flat, x.flat, y.flat)]
# col = PatchCollection(circles, array=c.flatten(), cmap="RdYlGn")
# ax.add_collection(col)
#
# ax.set(xticks=np.arange(M), yticks=np.arange(N),
#        xticklabels=xlabels, yticklabels=ylabels)
# ax.set_xticks(np.arange(M+1)-0.5, minor=True)
# ax.set_yticks(np.arange(N+1)-0.5, minor=True)
# ax.grid(which='minor')
#
# fig.colorbar(col)
# plt.show()
#
