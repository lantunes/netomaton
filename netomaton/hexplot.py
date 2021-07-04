from math import *

import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from .utils import get_activities_over_time_as_list
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection


def _oddr_offset_to_pixel(x, y, size=1):
    p_x = size * sqrt(3) * (x + 0.5 * (y & 1))
    p_y = size * 3 / 2 * y
    return p_x, p_y


def _evenr_offset_to_pixel(x, y, size=1):
    p_x = size * sqrt(3) * (x - 0.5 * (y & 1))
    p_y = size * 3 / 2 * y
    return p_x, p_y


def _get_scaled_colormap(triples, colormap, vmin, vmax):
    vals = [t[2] for t in triples]
    vmin = min(vals) if vmin is None else vmin
    vmax = max(vals) if vmax is None else vmax
    cmap = plt.get_cmap(colormap)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    return cm.ScalarMappable(norm=norm, cmap=cmap)


def _get_triples(activities):
    # using the “odd-r” horizontal layout offset coordinate system described in:
    #   https://www.redblobgames.com/grids/hexagons/#coordinates
    # here we get a list of tuples with three values: (x, y, node value)
    return [(x, y, val) for y, row in enumerate(activities) for x, val in enumerate(row)]


def plot_hex_grid(trajectory, shape=None, slice=-1, title='', colormap='Greys', vmin=None, vmax=None, edgecolor=None):
    activities = get_activities_over_time_as_list(trajectory)
    if shape is not None:
        activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
    triples = _get_triples(activities)
    has_odd_rows = (len(activities) % 2) != 0
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    m = _get_scaled_colormap(triples, colormap, vmin, vmax)
    for t in triples:
        x, y = _oddr_offset_to_pixel(t[0], t[1]) if has_odd_rows else _evenr_offset_to_pixel(t[0], t[1])
        hex = RegularPolygon((x, y), numVertices=6, radius=1.,
                             orientation=np.radians(60),
                             facecolor=m.to_rgba(t[2]), edgecolor=edgecolor)
        ax.add_patch(hex)
    ax.scatter([t[0] for t in triples], [t[1] for t in triples], marker='')
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.show()


def animate_hex(trajectory, title='', shape=None, save=False, interval=50, colormap='Greys',
                vmin=None, vmax=None, edgecolor=None):
    activities = get_activities_over_time_as_list(trajectory)
    if shape is not None:
        activities = np.reshape(activities, (len(activities), shape[0], shape[1]))
    triples = _get_triples(activities[0])
    has_odd_rows = (len(activities[0]) % 2) != 0
    fig, ax = plt.subplots(1)
    ax.set_aspect('equal')
    m = _get_scaled_colormap(triples, colormap, vmin, vmax)
    patches = []
    for t in triples:
        x, y = _oddr_offset_to_pixel(t[0], t[1]) if has_odd_rows else _evenr_offset_to_pixel(t[0], t[1])
        hex = RegularPolygon((x, y), numVertices=6, radius=1.,
                             orientation=np.radians(60), edgecolor=edgecolor)
        patches.append(hex)

    p = PatchCollection(patches, match_original=True, cmap=m.get_cmap())
    ax.add_collection(p)

    i = {'index': 0}
    def update(*args):
        i['index'] += 1
        if i['index'] == len(activities):
            i['index'] = 0
        new_triples = _get_triples(activities[i['index']])
        p.set_array(np.array([tr[2] for tr in new_triples]))
        return p,

    ax.scatter([t[0] for t in triples], [t[1] for t in triples], marker='')
    plt.gca().invert_yaxis()
    plt.title(title)

    ani = animation.FuncAnimation(fig, update, interval=interval, blit=True, save_count=len(activities))
    if save:
        ani.save('evolved.gif', dpi=80, writer="imagemagick")

    plt.show()

