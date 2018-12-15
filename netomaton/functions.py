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
    def __init__(self, activities, neighbour_indices, weights, current_activity):
        self._activities = activities
        self._neighbour_indices = neighbour_indices
        self._weights = weights
        self._current_activity = current_activity

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


def evolve(initial_conditions, adjacency_matrix, timesteps, activity_rule, connectivity_rule=ConnectivityRule.noop):
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
    :return: a tuple of the activities over time and the connectivities over time
    """
    if len(initial_conditions) != len(adjacency_matrix[0]):
        raise Exception("the length of the initial conditions list does not match the given adjacency matrix")
    activities_over_time = [initial_conditions]
    connectivities_over_time = [adjacency_matrix]

    num_cells = len(adjacency_matrix[0])

    for timestep in range(1, timesteps):
        last_activities = activities_over_time[-1]
        last_connectivities = connectivities_over_time[-1]
        activities = []

        last_connectivities_transposed = np.array(last_connectivities).T

        for cell_index in range(num_cells):
            ngh_activities = []
            ngh_cell_indices = []
            ngh_weights = []
            # use the transpose of the adjacency matrix to get the cells that are inputs to a given cell defined by a row
            for i, val in enumerate(last_connectivities_transposed[cell_index]):
                if val != 0.:
                    ngh_activities.append(last_activities[i])
                    ngh_cell_indices.append(i)
                    ngh_weights.append(val)
            activity = activity_rule(Neighbourhood(ngh_activities, ngh_cell_indices, ngh_weights, last_activities[cell_index]), cell_index, timestep)
            activities.append(activity)

        activities_over_time.append(activities)
        connectivities = connectivity_rule(last_connectivities, last_activities, timestep)
        connectivities_over_time.append(connectivities)

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
    return np.array([x]).tolist()


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
    return np.array([np.pad(np.array(rand_nums), (pad_left, pad_right), 'constant', constant_values=empty_value)]).tolist()


def plot_grid(activities, title=''):
    cmap = plt.get_cmap('Greys')
    plt.title(title)
    plt.imshow(activities, interpolation='none', cmap=cmap)
    plt.show()


def plot2d_animate(activities, title='', reshape=None, save=False):
    if reshape is not None:
        activities = np.reshape(activities, reshape)
    cmap = plt.get_cmap('Greys')
    fig = plt.figure()
    plt.title(title)
    im = plt.imshow(activities[0], animated=True, cmap=cmap)
    i = {'index': 0}
    def updatefig(*args):
        i['index'] += 1
        if i['index'] == len(activities):
            i['index'] = 0
        im.set_array(activities[i['index']])
        return im,
    ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
    if save:
        ani.save('evolved.gif', dpi=80, writer="imagemagick")
    plt.show()


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


