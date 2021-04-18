import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.collections as mcoll
from .state import State
try:
    import cPickle as pickle
except:
    import pickle


def plot_activities(trajectory_or_activities, shape=None, slice=-1, title='', colormap='Greys', vmin=None, vmax=None,
                    node_annotations=None, show_grid=False):
    if len(trajectory_or_activities) is 0:
        raise Exception("there are no activities")
    if isinstance(trajectory_or_activities[0], State):
        # trajectory_or_activities is a trajectory, convert it to an activities list
        activities = get_activities_over_time_as_list(trajectory_or_activities)
    else:
        activities = trajectory_or_activities
    if shape is not None:
        activities = _reshape_for_animation(activities, shape)
    plot_grid(activities, shape, slice, title, colormap, vmin, vmax, node_annotations, show_grid)


def get_activities_over_time_as_list(trajectory):
    activities = []
    for state in trajectory:
        ac = state.activities
        row = []
        if ac:
            for a in sorted(ac):
                row.append(ac[a])
            activities.append(row)
    return activities


def plot_grid(activities, shape=None, slice=-1, title='', colormap='Greys', vmin=None, vmax=None,
              node_annotations=None, show_grid=False):
    if shape is not None:
        activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
    cmap = plt.get_cmap(colormap)
    plt.title(title)
    plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)

    if node_annotations is not None:
        for i in range(len(node_annotations)):
            for j in range(len(node_annotations[i])):
                plt.text(j, i, node_annotations[i][j], ha="center", va="center", color="grey",
                         fontdict={'weight':'bold','size':6})

    if show_grid:
        plt.grid(which='major', axis='both', linestyle='-', color='grey', linewidth=0.5)
        plt.xticks(np.arange(-.5, len(activities[0]), 1), "")
        plt.yticks(np.arange(-.5, len(activities), 1), "")
        plt.tick_params(axis='both', which='both', length=0)

    plt.show()


def plot_grid_multiple(ca_list, shape=None, slice=-1, titles=None, colormap='Greys', vmin=None, vmax=None):
    cmap = plt.get_cmap(colormap)
    for i in range(0, len(ca_list)):
        plt.figure(i)
        if titles is not None:
            plt.title(titles[i])
        activities = list(ca_list[i])
        if shape is not None:
            activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
        plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)
    plt.show()


def animate_activities(trajectory_or_activities, title='', shape=None, save=False, interval=50, colormap='Greys',
                       vmin=None, vmax=None, show_grid=False, show_margin=True, scale=0.6, dpi=80):
    if len(trajectory_or_activities) is 0:
        raise Exception("there are no activities")
    if isinstance(trajectory_or_activities[0], State):
        # trajectory_or_activities is a trajectory, convert it to an activities list
        activities = get_activities_over_time_as_list(trajectory_or_activities)
    else:
        activities = trajectory_or_activities
    if shape is not None:
        activities = _reshape_for_animation(activities, shape)
    cmap = plt.get_cmap(colormap)
    fig, ax = plt.subplots()
    plt.title(title)
    if not show_margin:
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

    grid_linewidth = 0.0
    if show_grid:
        plt.xticks(np.arange(-.5, len(activities[0][0]), 1), "")
        plt.yticks(np.arange(-.5, len(activities[0]), 1), "")
        plt.tick_params(axis='both', which='both', length=0)
        grid_linewidth = 0.5

    vertical = np.arange(-.5, len(activities[0][0]), 1)
    horizontal = np.arange(-.5, len(activities[0]), 1)
    lines = ([[(x, y) for y in (-.5, horizontal[-1])] for x in vertical] +
             [[(x, y) for x in (-.5, vertical[-1])] for y in horizontal])
    grid = mcoll.LineCollection(lines, linestyles='-', linewidths=grid_linewidth, color='grey')
    ax.add_collection(grid)

    im = plt.imshow(activities[0], animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
    if not show_margin:
        baseheight, basewidth = im.get_size()
        fig.set_size_inches(basewidth*scale, baseheight*scale, forward=True)

    i = {'index': 0}
    def updatefig(*args):
        i['index'] += 1
        if i['index'] == len(activities):
            i['index'] = 0
        im.set_array(activities[i['index']])
        return im, grid
    ani = animation.FuncAnimation(fig, updatefig, interval=interval, blit=True, save_count=len(activities))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer="imagemagick")
    plt.show()


def animate_plot1D(x, y, save=False, interval=50, dpi=80):
    if isinstance(y[0], State):
        # y is a trajectory, convert it to an activities list
        y = get_activities_over_time_as_list(y)
    fig1 = plt.figure()
    line, = plt.plot(x, y[0])
    def update_line(activity):
        line.set_data(x, activity)
        return line,
    ani = animation.FuncAnimation(fig1, update_line, frames=y, blit=True, interval=interval)
    if save:
        ani.save('plot.gif', dpi=dpi, writer="imagemagick")
    plt.show()


def _reshape_for_animation(activities, shape):
    if len(shape) == 1:
        assert shape[0] == len(activities[0]), "shape must equal the length of an activity vector"
        new_activities = []
        for i, a in enumerate(activities):
            new_activity = []
            new_activity.extend(activities[0:i+1])
            while len(new_activity) < len(activities):
                new_activity.append([0]*len(activities[0]))
            new_activities.append(new_activity)
        return np.array(new_activities)
    elif len(shape) == 2:
        return np.reshape(activities, (len(activities), shape[0], shape[1]))
    else:
        raise Exception("shape must be a tuple of length 1 or 2")


def plot_network(network, layout="shell", with_labels=True, node_color="#1f78b4", node_size=300):
    G = network.to_networkx()
    if layout == "shell":
        nx.draw_shell(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
    elif layout == "spring":
        nx.draw_spring(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
    elif isinstance(layout, dict):
        nx.draw(G, pos=layout, with_labels=with_labels, node_color=node_color, node_size=node_size)
    else:
        raise Exception("unsupported layout: %s" % layout)
    plt.show()


def animate_network(trajectory, save=False, interval=50, dpi=80, layout="shell",
                    with_labels=True, node_color="b", node_size=30):
    fig, ax = plt.subplots()

    def update(state):
        ax.clear()

        network = state.network
        G = nx.MultiDiGraph()
        for n in network.nodes:
            G.add_node(n)
        for edge in network.edges:
            G.add_edge(edge[0], edge[1])

        if layout == "shell":
            nx.draw_shell(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
        elif layout == "spring":
            nx.draw_spring(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
        elif isinstance(layout, dict):
            nx.draw(G, pos=layout, with_labels=with_labels, node_color=node_color, node_size=node_size)
        else:
            raise Exception("unsupported layout: %s" % layout)

    ani = animation.FuncAnimation(fig, update, frames=trajectory, interval=interval,
                                  save_count=len(trajectory))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer="imagemagick")
    plt.show()
