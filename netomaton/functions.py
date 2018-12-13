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


