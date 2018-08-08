from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import h5py
import sys
import getopt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib import animation, rc
from mpl_toolkits.axes_grid1 import make_axes_locatable
import textwrap
import random
import FileDialog


#plt.switch_backend('agg')

if len(sys.argv[1]) == 3:
    scan_id = sys.argv[1]
    filename = "files/patch1_" + str(scan_id) + "_map.h5"
else:
    filename = sys.argv[1]

def readMap(filename):
        dfile   = h5py.File(filename,'r')
        nx      = dfile['n_x'];      nx  = np.array(nx).astype(int)
        ny      = dfile['n_y'];      ny  = np.array(ny).astype(int)
        x       = dfile['x'];         x  = np.array(x[:]).astype(float)
        y       = dfile['y'];         y  = np.array(y[:]).astype(float)
        maps    = dfile['map'];    maps  = np.array(maps[...]).astype(float)
        hit     = dfile['nhit'];    hit  = np.array(hit[...]).astype(float)
        rms     = dfile['rms'];     rms  = np.array(rms[...]).astype(float)

        return x, y, maps, hit, rms

def swap_xy(my_array):

        new_array = np.zeros((len(my_array[0]), len(my_array)))
        #my_array[:, 0], my_array[:, 1] = my_array[:, 1], my_array[:, 0].copy()
        for i in range(len(my_array[0])):
            new_array[i, :] = my_array[:, i]
        return new_array


def makeMap_one(x, y, mapData, hitData):
        cm.viridis.set_bad('w',1.) #color of masked elements
        mapData = np.ma.masked_where(hitData < 1., mapData)
        return mapData


def setup_one(filename, sb, freq):
        print 'Plotting map for sb ', sb, ', freq ', freq
        x, y, maps, hit, rms= readMap(filename)

        var = maps[sb-1,freq-1,:,:]
        hitData = hit[sb-1,freq-1,:,:]#;  hitData = np.swapaxes(hitData,0,1)

        var = swap_xy(var)
        hitData = swap_xy(hitData)

        x_min = x[1]
        x_max = x[-1] + (x[1]-x[0])
        y_min = y[1]
        y_max = y[-1] + (y[1]-y[0])

        return makeMap_one(x, y, var, hitData), x_min, x_max, y_min, y_max


def expand_map(filename):
    f = h5py.File(filename, 'r+')
    data = f[f.keys()[0]]
    nsb = np.shape(data)[0]
    nfreq = np.shape(data)[1]
    nx = np.shape(data)[2]
    ny = np.shape(data)[3]
    n = max(nx, ny)
    map = np.zeros((nsb, nfreq, n, n))
    map[:, :, :nx, :ny] = data[:, :, :, :]
    """
    for i in range(nsb):
        for j in range(nfreq):
            for k in range(nx):
                for l in range(ny):
                    if map[i, j, k, l] != 0:
                        print map[i, j, k, l]
    sd
    """
    return map, nsb, nfreq, nx, ny

map, nsb, nfreq, nx, ny = expand_map(filename)
nsb = 1
nfreq = 1
n = max(nx, ny)
x = np.zeros(n*n)
y = np.zeros(n*n)
z = np.zeros(n*n)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#for i in range(nsb):
#    for j in range(nfreq):
for k in range(n):
    x[k*n:n*(1+k)-1] = k
    for l in range(n):
        y[n*k + l] = l
        z[n*k + l] = map[0,0,k,l]
        #if map[i,j,k,l] != 0:
        #    print i,j,k,l
ax.scatter(x, y, c=z, s=100, marker=".",edgecolor='', cmap="Greys")
#plt.savefig("test.png")
plt.show()
"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
map, nsb, nfreq, nx, ny = expand_map(filename)
for i in range(nsb):
    for j in range(nfreq
        ax.scatter(range(nx), range(ny), map[i, j], extent=(x_min[count], x_max[count], y_min[count], y_max[count]), interpolation='nearest',cmap=plt.cm.viridis,origin='lower')
        count += 1
plt.show()
"""
