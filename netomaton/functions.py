import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from .connectivity_rule import *
import multiprocessing
from multiprocessing import Pool
import scipy.sparse as sparse


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


def evolve(initial_conditions, adjacency_matrix, activity_rule, timesteps=None, input=None, connectivity_rule=None,
           perturbation=None, parallel=False, processes=None):
    """
    Evolves a network defined by the given adjacency matrix with the given initial conditions, for the specified
    number of timesteps, using the given activity and connectivity rules. Note that if A(t) is the adjacency matrix at
    timestep t, and S(t) is the network activity vector at timestep t, and F is a function defining a connectivity
    rule, and G is a function describing an activity rule, then A(t+1) and S(t+1) are defined as follows:
    A(t+1) = F(A(t), S(t))
    S(t+1) = G(A(t), S(t))
    :param initial_conditions: the initial activities of the network
    :param adjacency_matrix: the adjacency matrix defining the network topology
    :param activity_rule: the rule that will determine the activity of a cell in the network
    :param timesteps: the number of steps in the evolution of the network; Note that the initial state, specified by the
                      initial_conditions, is considered the result of a timestep, so that the activity_rule is invoked
                      t - 1 times; for example, if timesteps is 6, then the initial state is considered the result of
                      the first timestep (t=0), and the activity_rule will be invoked five times; the activity_rule
                      (and any perturbation) will receive the current timestep number each time it is invoked;
                      specifying the timesteps implies an automaton that evolves on its own, in the absence of any
                      external driving signal
    :param input: a list representing the input to the network at a particular timestep; each item in the list
                  contains the input for each cell in the network for a particular timestep; the activity_rule (and any
                  perturbation) will receive the current input value for a given cell instead of the current timestep
                  number itself, when the input parameter is provided; either the input or timesteps parameter must be
                  provided, but not both; if the input parameter is provided, it will override the timesteps parameter,
                  and the timesteps parameter will have no effect; the first item in the input list is given to the
                  network at t=1, the second at t=2, etc. (i.e. no input is specified for the initial state);
                  specifying the input implies an automaton whose evolution is driven by an external signal
    :param connectivity_rule: the rule that will determine the connectivity of the network
    :param perturbation: a function that defines a perturbation applied as the system evolves; the function accepts
                         three parameters: c, which represents the cell index, t, which represents the timestep, and a,
                         which represents the computed activity for the cell given by c. The function must return the
                         new activity for cell c at timestep t.
    :param parallel: whether the evolution of the cells should be performed in parallel;
                     Note: the activity_rule function must be safe to use concurrently, as it will
                     be invoked concurrently from different processes when this flag is set to True (the same is true
                     for the perturbation function); this generally means that the activity rule (and perturbation)
                     function cannot keep any state; some built-in rules, such as ReversibleRule and AsynchronousRule,
                     won't work correctly when 'parallel' is True
    :param processes: the number of processes to start for parallel execution, if 'parallel' is set to True;
                      the number of CPUs will be used if 'processes' is not provided and 'parallel' is True
    :return: a tuple of the activities over time and the connectivities over time
    """
    if len(initial_conditions) != len(adjacency_matrix[0]):
        raise Exception("the length of the initial conditions list does not match the given adjacency matrix")

    if timesteps is None and input is None:
        raise Exception("either the timesteps or input must be provided")

    if connectivity_rule is not None:
        return _evolve_both(initial_conditions, adjacency_matrix, activity_rule, timesteps, input, connectivity_rule, perturbation)
    else:
        if parallel:
            return _evolve_activities_parallel(initial_conditions, adjacency_matrix, activity_rule, timesteps, input,
                                               perturbation, processes)
        else:
            return _evolve_activities(initial_conditions, adjacency_matrix, activity_rule, timesteps, input, perturbation)


def _evolve_activities(initial_conditions, adjacency_matrix, activity_rule, timesteps, input, perturbation):
    if input is not None:
        timesteps = len(input) + 1

    activities_over_time = np.zeros((timesteps, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
    activities_over_time[0] = initial_conditions

    num_cells = len(adjacency_matrix[0])
    connectivities_sparse = sparse.csc_matrix(adjacency_matrix)
    nonzero_index_map = {}
    weight_map = {}
    for c in range(num_cells):
        sparse_col =  connectivities_sparse.getcol(c)
        nonzero_index_map[c] = sparse_col.nonzero()[0].tolist()
        weight_map[c] = sparse_col.data.tolist()

    for t in range(1, timesteps):
        last_activities = activities_over_time[t - 1]

        for c in range(num_cells):
            nonzero_indices = nonzero_index_map[c]
            activities = [last_activities[i] for i in nonzero_indices]
            weights = weight_map[c]
            cell_in = t if input is None else input[t-1][c]
            activities_over_time[t][c] = activity_rule(Neighbourhood(activities, nonzero_indices, weights, last_activities[c]), c, cell_in)
            if perturbation is not None:
                activities_over_time[t][c] = perturbation(c, activities_over_time[t][c], cell_in)

    return activities_over_time, [adjacency_matrix]*timesteps


def _process_cells(cell_indices, t, last_activities):
    global nonzero_index_map
    global weight_map
    global fn_activity
    global fn_perturb
    global net_inputs
    results = {}
    for c in cell_indices:
        nonzero_indices = nonzero_index_map[c]
        activities = [last_activities[i] for i in nonzero_indices]
        weights = weight_map[c]
        cell_in = t if net_inputs is None else net_inputs[t-1][c]
        cell_activity = fn_activity(Neighbourhood(activities, nonzero_indices, weights, last_activities[c]), c, cell_in)
        if fn_perturb is not None:
            cell_activity = fn_perturb(c, cell_activity, cell_in)
        results[c] = cell_activity
    return results


def _evolve_activities_parallel(initial_conditions, adjacency_matrix, activity_rule, timesteps, input,
                                perturbation, processes):
    if input is not None:
        timesteps = len(input) + 1

    activities_over_time = np.zeros((timesteps, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
    activities_over_time[0] = initial_conditions

    num_cells = len(adjacency_matrix[0])
    connectivities_sparse = sparse.csc_matrix(adjacency_matrix)
    global nonzero_index_map
    nonzero_index_map = {}
    global weight_map
    weight_map = {}
    for c in range(num_cells):
        sparse_col = connectivities_sparse.getcol(c)
        nonzero_index_map[c] = sparse_col.nonzero()[0].tolist()
        weight_map[c] = sparse_col.data.tolist()

    global fn_activity
    fn_activity = activity_rule
    global fn_perturb
    fn_perturb = perturbation

    global net_inputs
    net_inputs = input

    if processes is None:
        processes = multiprocessing.cpu_count()
    cell_index_chunks = np.array_split(np.array(range(num_cells)), processes)
    pool = Pool(processes=processes)

    for t in range(1, timesteps):
        last_activities = activities_over_time[t - 1]

        args = [(chunk, t, last_activities) for chunk in cell_index_chunks]
        map_result = pool.starmap_async(_process_cells, args)

        for results in map_result.get():
            for c in results.keys():
                activities_over_time[t][c] = results[c]

    pool.close()
    pool.join()

    return activities_over_time, [adjacency_matrix]*timesteps


def _evolve_both(initial_conditions, adjacency_matrix, activity_rule, timesteps, input,
                 connectivity_rule=ConnectivityRule.noop, perturbation=None):
    if input is not None:
        timesteps = len(input) + 1

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
            cell_in = t if input is None else input[t-1][c]
            activities_over_time[t][c] = activity_rule(Neighbourhood(activities, nonzero_indices, weights, last_activities[c]), c, cell_in)
            if perturbation is not None:
                activities_over_time[t][c] = perturbation(c, activities_over_time[t][c], cell_in)

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


def plot_grid(activities, shape=None, slice=-1, title='', colormap='Greys', vmin=None, vmax=None,
              cell_annotations=None, show_grid=False):
    if shape is not None:
        activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
    cmap = plt.get_cmap(colormap)
    plt.title(title)
    plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)

    if cell_annotations is not None:
        for i in range(len(cell_annotations)):
            for j in range(len(cell_annotations[i])):
                plt.text(j, i, cell_annotations[i][j], ha="center", va="center", color="grey",
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


