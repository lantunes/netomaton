import networkx as nx
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.collections as mcoll
import collections
from .state import State
from .substitution_system import SubstitutionSystem
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
                    with_labels=True, with_arrows=True, node_color="b", node_size=30):
    fig, ax = plt.subplots()

    def update(arg):
        ax.clear()

        i, state = arg

        color = node_color[i] if type(node_color) == dict else node_color

        network = state.network
        G = nx.MultiDiGraph()
        for n in network.nodes:
            G.add_node(n)
        for edge in network.edges:
            G.add_edge(edge[0], edge[1])

        state_layout = layout[i] if type(layout) == list or type(layout) == tuple else layout

        if state_layout == "shell":
            nx.draw_shell(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif state_layout == "spring":
            nx.draw_spring(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif state_layout == "planar":
            nx.draw_planar(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif state_layout == "kamada-kawai":
            nx.draw_kamada_kawai(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif isinstance(state_layout, dict):
            nx.draw(G, pos=state_layout, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        else:
            raise Exception("unsupported layout: %s" % state_layout)

    ani = animation.FuncAnimation(fig, update, frames=list(enumerate(trajectory)), interval=interval,
                                  save_count=len(trajectory))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer="imagemagick")
    plt.show()


def plot1D(x, y, color=None, label=None, xlabel=None, ylabel=None, xlim=None, ylim=None, twinx=False,
           legend=None, tight_layout=None, title=None):
    """
    Creates a 1D plot of the given x and y values.

    :param x: A list representing the values of the x-axis.

    :param y: A list representing the values of the y-axis. If the values of this list are also lists, then each will
              be plotted as a separate series on the y-axis.

    :param color: A string, representing the color of the series, or a list of colors, representing the color of each
                   series to be plotted. The number of colors must match the number of series. The color values must
                   be recognizable by Matplotlib.

    :param label: A string or number, or a list of strings or numbers, representing the labels of each series to be
                  plotted. The number of labels must match the number of series.

    :param xlabel: A string representing the label of the x-axis.

    :param ylabel: A string, or list of at most two strings, representing the label(s) of the y-axis.

    :param xlim: A 2-tuple of numbers, representing the limits of the x-axis.

    :param ylim: A 2-tuple of numbers, or a list of at most two 2-tuples of numbers, representing the
                 limits of the y-axis.

    :param twinx: If True, the provided y series will be plotted on two separate y-axes, and there must
                  be at least two series of y values provided. If there are more than two series of y values,
                  then each series will be plotted on alternating y-axes. (Default is False)

    :param legend: A dict, or a list of at most two dicts, representing the arguments to the legend
                   function of Matplotlib.

    :param tight_layout: A dict representing the arguments to the tight_layout function of Matplotlib.

    :param title: The plot title.
    """
    axes = []
    fig, ax1 = plt.subplots()
    axes.append(ax1)
    if twinx:
        axes.append(ax1.twinx())
        if len(y) < 2:
            raise Exception("there must be at least two series of y values provided")
        for _y in y:
            if not isinstance(_y, (list, np.ndarray)):
                raise Exception("an item in y must be a list representing a y series")

    current_axis_idx = 0
    # assume that the first value type in y is representative of all the value types in y
    is_multiseries = isinstance(y[0], (list, np.ndarray))

    def _get_item(items, i):
        if isinstance(items, str):
            return items
        if isinstance(items, collections.Sequence):
            return items[i]
        return items

    if not is_multiseries:
        y = [y]

    for i, y_series in enumerate(y):
        current_axis = axes[current_axis_idx % len(axes)]
        plot_args = {}
        if label:
            plot_args["label"] = _get_item(label, i)
        if color:
            plot_args["color"] = _get_item(color, i)
        current_axis.plot(x, y_series, **plot_args)
        if xlabel:
            current_axis.set_xlabel(xlabel)
        if ylabel:
            ylabel_args = {}
            if color:
                ylabel_args["color"] = _get_item(color, i)
            current_axis.set_ylabel(_get_item(ylabel, i % 2), **ylabel_args)
        if xlim:
            current_axis.set_xlim(xlim)
        if ylim:
            current_axis.set_ylim(_get_item(ylim, i % 2))
        if legend:
            current_axis.legend(**legend)

        current_axis_idx += 1

    if tight_layout:
        plt.tight_layout(**tight_layout)

    if title:
        plt.title(title)

    plt.show()


def poincare_plot(activities, timesteps, xlabel=None, ylabel=None, xlim=None, ylim=None, title=None):
    """
    Create a Poincaré plot.

    :param activities: A list of activities. If the values of this list are also lists, then each will
                       be plotted as a separate series.

    :param timesteps: The number of timesteps in the trajectory to consider, starting from the end.

    :param xlabel: A string representing the label of the x-axis.

    :param ylabel: A string representing the label of the y-axis.

    :param xlim: A 2-tuple of numbers, representing the limits of the x-axis.

    :param ylim: A 2-tuple of numbers, or a list of at most two 2-tuples of numbers, representing the
                 limits of the y-axis.

    :param title: The plot title.
    """
    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # assume that the first value type in y is representative of all the value types in y
    is_multiseries = isinstance(activities[0], (list, np.ndarray))
    if is_multiseries:
        ax.set_prop_cycle(color=[cm(1. * i / len(activities)) for i in range(len(activities))])
    else:
        activities = [activities]
    for a in activities:
        x = []
        y = []
        for t in range(timesteps - 1):
            x.append(a[-timesteps:][t])
            y.append(a[-timesteps:][t + 1])
        plt.scatter(x, y, s=1)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.show()


def bifurcation_plot(x, trajectories, timesteps, xlabel=None, ylabel=None, title=None):
    """
    Create a bifurcation plot.

    :param x: A list representing the values of the x-axis.

    :param trajectories: A list of lists. Each inner list is a sequence of activities representing a trajectory.

    :param timesteps: The number of timesteps in the trajectory to consider, starting from the end.

    :param xlabel: A string representing the label of the x-axis.

    :param ylabel: A string representing the label of the y-axis.

    :param title: The plot title.
    """
    y = []
    for t in trajectories:
        y.append(np.unique(t[-timesteps:]))
    for x_e, y_e in zip(x, y):
        plt.scatter([x_e] * len(y_e), y_e, color="b", s=1)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.show()


def plot_degree_distribution(network, xlabel="Node degree", ylabel_freq="Frequency", ylabel_prob="Probability",
                             in_degree=False, out_degree=False,
                             equation=None, equation_x=0.51, equation_y=0.76, equation_text="", equation_color="r",
                             color="r", title=None):
    """
    Create a node degree distribution plot for the given network.

    :param network: A Netomaton Network instance.

    :param xlabel: The x-axis label.

    :param ylabel_freq: The frequency y-axis label.

    :param ylabel_prob: The probability y-axis label.

    :param in_degree: If True, the in-degree will be used. (default is False)

    :param out_degree: If True, the out-degree will be used. (default is False)

    :param equation: A callable that computes the degree distribution, given a node degree.

    :param equation_x: The equation's x coordinate.

    :param equation_y: The equation's y coordinate.

    :param equation_text: The equation to display.

    :param equation_color: The equation text's color. It must be a valid Matplotlib color.

    :param color: The color to use for the plot. It must be a valid Matplotlib color.

    :param title: The plot's title.
    """
    degree_counts = {}
    for node in network.nodes:
        if in_degree:
            degree = network.in_degree(node)
        elif out_degree:
            degree = network.out_degree(node)
        else:
            degree = network.degree(node)

        if degree not in degree_counts:
            degree_counts[degree] = 0
        degree_counts[degree] += 1

    x = [i for i in range(1, max(degree_counts) + 1)]
    height = [degree_counts[i] if i in degree_counts else 0 for i in x]
    plt.bar(x, height)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel_freq)

    if equation:
        y = [equation(k) for k in x]
        plt.twinx()
        plt.plot(x, y, color=color)
        plt.ylabel(ylabel_prob)
        plt.text(equation_x, equation_y, equation_text, transform=plt.gca().transAxes, color=equation_color)

    if title:
        plt.title(title)

    plt.show()


def ncr(n, r):
    """
    Returns the number of ways to choose r items from n items without repetition and without order.

    :param n: A non-negative integer.

    :param r: A non-negative integer.

    :return: An integer representing the number of ways to choose r items from n items without repetition
             and without order.
    """
    if not isinstance(n, int) or n < 0:
        raise Exception("n must be a non-negative int")
    if not isinstance(r, int) or r < 0:
        raise Exception("r must be a non-negative int")
    if n < r:
        return 0
    f = math.factorial
    return f(n) // f(r) // f(n-r)


def plot_L_system(state, turtle, bindings, **kwargs):
    _render_L_system(state, bindings)
    turtle.plot(**kwargs)


def animate_L_system(state, turtle, bindings, **kwargs):
    _render_L_system(state, bindings)
    turtle.animate(**kwargs)


def _render_L_system(state, bindings):
    state = SubstitutionSystem.to_string([state])[0]
    for s in state:
        instructions = bindings[s]
        if not isinstance(instructions, list):
            instructions = [instructions]
        for instruction in instructions:
            if callable(instruction):
                instruction()
            else:
                fn, *args = instruction
                fn(*args)


def binarize_for_plotting(activities):
    """
    Expects a list of lists of single numbers representing the activities (e.g. [[2], [35], [12]]),
    and returns a list of lists of the binarized versions of the given numbers, left-padded with
    zeroes. (e.g. [[0, 0, 0, 0, 1, 0], [1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0]])

    :param activities: the activities as a list of lists of single numbers

    :return: a list of lists of the binary versions of the numbers, left-padded with zeroes
    """
    activities = [[int(x) for x in bin(int(a[0]))[2:]] for a in activities]
    max_len = np.max([len(a) for a in activities])
    return np.asarray([np.pad(a, (max_len - len(a), 0), 'constant', constant_values=0) for a in activities])
