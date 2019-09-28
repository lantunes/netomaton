import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


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


def animate(activities, title='', shape=None, save=False, interval=50, colormap='Greys', vmin=None, vmax=None):
    if shape is not None:
        activities = _reshape_for_animation(activities, shape)
    cmap = plt.get_cmap(colormap)
    fig = plt.figure()
    plt.title(title)
    im = plt.imshow(activities[0], animated=True, cmap=cmap, vmin=vmin, vmax=vmax)
    i = {'index': 0}
    def updatefig(*args):
        i['index'] += 1
        if i['index'] == len(activities):
            i['index'] = 0
        im.set_array(activities[i['index']])
        return im,
    ani = animation.FuncAnimation(fig, updatefig, interval=interval, blit=True, save_count=len(activities))
    if save:
        ani.save('evolved.gif', dpi=80, writer="imagemagick")
    plt.show()


def animate_plot1D(x, y, save=False, interval=50):
    fig1 = plt.figure()
    line, = plt.plot(x, y[0])
    def update_line(activity):
        line.set_data(x, activity)
        return line,
    ani = animation.FuncAnimation(fig1, update_line, frames=y, blit=True, interval=interval)
    if save:
        ani.save('plot.gif', dpi=80, writer="imagemagick")
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


def render_network(adjacency_matrix):
    G = nx.DiGraph()
    for n, _ in enumerate(adjacency_matrix):
        G.add_node(n)
    for row_index, row in enumerate(adjacency_matrix):
        for node_index, val in enumerate(row):
            if val != 0.:
                G.add_edge(row_index, node_index)

    nx.draw_shell(G, with_labels=True)
    plt.show()
