import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .connectivity_rule import *


class Neighbourhood(object):
    """
    A neighbourhood consists of the states, identities (as cell indices), and adjancency matrix weights of the cells
    that influence a given cell. Each of the properties (i.e. activities, cell_indices, weights) are represented as
    lists. Each of the lists are of the same size, and the first item in each list corresponds to the first cell in the
    neighbourhood, etc. The neighbourhood of a cell also contains the cell's current activity (i.e. the activity as of
    the last timestep).
    """
    def __init__(self, activities, neighbour_indices, weights, current_activity, perturbation=None):
        self._activities = activities
        self._neighbour_indices = neighbour_indices
        self._weights = weights
        self._current_activity = current_activity
        self._perturbation = perturbation

    @property
    def activities(self):
        return self._activities

    @property
    def neighbour_indices(self):
        return self._neighbour_indices

    @property
    def weights(self):
        return self._weights

    @property
    def current_activity(self):
        return self._current_activity

    @property
    def perturbation(self):
        return self._perturbation


def evolve(initial_conditions, adjacency_matrix, timesteps, activity_rule, connectivity_rule=None, perturbation=None):
    """
    Evolves a network defined by the given adjacency matrix with the given initial conditions, for the specified
    number of timesteps, using the given activity and connectivity rules. Note that if A(t) is the adjacency matrix at
    timestep t, and S(t) is the network activity vector at timestep t, and F is a function defining a connectivity
    rule, and G is a function describing an activity rule, then A(t+1) and S(t+1) are defined as follows:
    A(t+1) = F(A(t), S(t))
    S(t+1) = G(A(t), S(t))
    :param initial_conditions: the initial activities of the network
    :param adjacency_matrix: the adjacency matrix defining the network
    :param timesteps: the number of steps in the evolution of the network
    :param activity_rule: the rule that will determine the activity of a cell in the network
    :param connectivity_rule: the rule that will determine the connectivity of the network
    :param perturbation: a function that defines a perturbation applied as the system evolves; the function accepts
                         three parameters: c, which represents the cell index, t, which represents the timestep, and a,
                         which represents the computed activity for the cell given by c. The function must return the
                         new activity for cell c at timestep t.
    :return: a tuple of the activities over time and the connectivities over time
    """
    if len(initial_conditions) != len(adjacency_matrix[0]):
        raise Exception("the length of the initial conditions list does not match the given adjacency matrix")

    if connectivity_rule is not None:
        return _evolve_both(initial_conditions, adjacency_matrix, timesteps, activity_rule, connectivity_rule, perturbation)
    else:
        return _evolve_activities(initial_conditions, adjacency_matrix, timesteps, activity_rule, perturbation)


def _evolve_activities(initial_conditions, adjacency_matrix, timesteps, activity_rule, perturbation=None):
    activities_over_time = np.zeros((timesteps, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
    activities_over_time[0] = initial_conditions

    num_cells = len(adjacency_matrix[0])
    connectivities_transposed = np.array(adjacency_matrix).T

    nonzeros = np.nonzero(connectivities_transposed)
    index_map = {i: [] for i in range(num_cells)}
    [index_map[idx].append(nonzeros[1][i]) for i, idx in enumerate(nonzeros[0])]

    for t in range(1, timesteps):
        last_activities = activities_over_time[t - 1]

        for c in range(num_cells):
            # use the transpose of the adjacency matrix to get the cells that are inputs to a given cell defined by a row
            row = connectivities_transposed[c]
            nonzero_indices = index_map[c]
            activities = last_activities[nonzero_indices]
            weights = row[nonzero_indices]
            activities_over_time[t][c] = activity_rule(Neighbourhood(activities, nonzero_indices, weights, last_activities[c]), c, t)
            if perturbation is not None:
                activities_over_time[t][c] = perturbation(c, activities_over_time[t][c], t)

    return activities_over_time, [adjacency_matrix]*timesteps


def _evolve_both(initial_conditions, adjacency_matrix, timesteps, activity_rule, connectivity_rule=ConnectivityRule.noop, perturbation=None):
    activities_over_time = np.zeros((timesteps, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
    activities_over_time[0] = initial_conditions

    connectivities_over_time = np.zeros((timesteps, len(adjacency_matrix), len(adjacency_matrix)), dtype=np.dtype(type(adjacency_matrix[0][0])))
    connectivities_over_time[0] = adjacency_matrix

    num_cells = len(adjacency_matrix[0])

    for t in range(1, timesteps):
        last_activities = activities_over_time[t - 1]
        last_connectivities = connectivities_over_time[t - 1]

        last_connectivities_transposed = np.array(last_connectivities).T

        nonzeros = np.nonzero(last_connectivities_transposed)
        index_map = {i: [] for i in range(num_cells)}
        [index_map[idx].append(nonzeros[1][i]) for i, idx in enumerate(nonzeros[0])]

        for c in range(num_cells):
            # use the transpose of the adjacency matrix to get the cells that are inputs to a given cell defined by a row
            row = last_connectivities_transposed[c]
            nonzero_indices = index_map[c]
            activities = last_activities[nonzero_indices]
            weights = row[nonzero_indices]
            activities_over_time[t][c] = activity_rule(Neighbourhood(activities, nonzero_indices, weights, last_activities[c]), c, t)
            if perturbation is not None:
                activities_over_time[t][c] = perturbation(c, activities_over_time[t][c], t)

        connectivities = connectivity_rule(last_connectivities, last_activities, t)
        connectivities_over_time[t] = connectivities

    return activities_over_time, connectivities_over_time


def init_simple(size, val=1, dtype=np.int):
    """
    Returns an array initialized with zeroes, with its center value set to the specified value, or 1 by default.
    :param size: the size of the array to be created
    :param val: the value to be used in the center of the array (1, by default)
    :param dtype: the data type
    :return: a vector with shape (1, size), with its center value initialized to the specified value, or 1 by default
    """
    x = np.zeros(size, dtype=dtype)
    x[len(x)//2] = val
    return x.tolist()


def init_random(size, k=2, n_randomized=None, empty_value=0, dtype=np.int):
    """
    Returns a randomly initialized array with values consisting of numbers in {0,...,k - 1}, where k = 2 by default.
    If dtype is not an integer type, then values will be uniformly distributed over the half-open interval [0, k - 1).
    :param size: the size of the array to be created
    :param k: the number of states in the cellular automaton (2, by default)
    :param n_randomized: the number of randomized sites in the array; this value must be >= 0 and <= size, if specified;
                         if this value is not specified, all sites in the array will be randomized; the randomized sites
                         will be centered in the array, while all others will have an empty value
    :param empty_value: the value to use for non-randomized sites (0, by default)
    :param dtype: the data type
    :return: a vector with shape (1, size), randomly initialized with numbers in {0,...,k - 1}
    """
    if n_randomized is None:
        n_randomized = size
    if n_randomized > size or n_randomized < 0:
        raise Exception("the number of randomized sites, if specified, must be >= 0 and <= size")
    pad_left = (size - n_randomized) // 2
    pad_right = (size - n_randomized) - pad_left
    if np.issubdtype(dtype, np.integer):
        rand_nums = np.random.randint(k, size=n_randomized, dtype=dtype)
    else:
        rand_nums = np.random.uniform(0, k - 1, size=n_randomized).astype(dtype)
    return np.array(np.pad(np.array(rand_nums), (pad_left, pad_right), 'constant', constant_values=empty_value)).tolist()


def init_simple2d(rows, cols, val=1, dtype=np.int):
    """
    Returns a list initialized with zeroes, with its center value set to the specified value, or 1 by default, when the
    list is reshaped according to the given number of rows and columns.
    :param rows: the number of rows
    :param cols: the number of columns
    :param val: the value to be used in the center of the matrix (1, by default)
    :param dtype: the data type
    :return: a list with size rows * cols, with the center value initialized to the specified value, or 1 by default
    """
    x = np.zeros((rows, cols), dtype=dtype)
    x[x.shape[0]//2][x.shape[1]//2] = val
    return np.array(x).reshape(rows * cols).tolist()


def plot_grid(activities, shape=None, slice=-1, title='', colormap='Greys', vmin=None, vmax=None):
    if shape is not None:
        activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
    cmap = plt.get_cmap(colormap)
    plt.title(title)
    plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)
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
        for cell_index, val in enumerate(row):
            if val != 0.:
                G.add_edge(row_index, cell_index)

    nx.draw_shell(G, with_labels=True)
    plt.show()


