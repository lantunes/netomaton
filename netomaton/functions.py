import collections
import multiprocessing
from multiprocessing import Pool

import numpy as np
import scipy.sparse as sparse

from .connectivity_rule import *


class Neighbourhood(object):
    """
    A neighbourhood consists of the states, identities (as cell indices), and adjancency matrix weights of the cells
    that influence a given cell. Each of the properties (i.e. activities, neighbour_indices, weights) are represented as
    lists. Each of the lists are of the same size, and the first item in each list corresponds to the first cell in the
    neighbourhood, etc. The neighbourhood of a cell also contains the cell's current activity (i.e. the activity as of
    the last timestep).
    """
    def __init__(self, activities, neighbour_indices, weights, current_activity, perturbation=None, past_activities=None):
        self._activities = activities
        self._neighbour_indices = neighbour_indices
        self._weights = weights
        self._current_activity = current_activity
        self._perturbation = perturbation
        self._past_activities = past_activities

    def activity_of(self, cell_index):
        """
        Returns the activity of the cell with the given cell index.
        :param cell_index: the index of the cell whose activity is being requested
        :return: the activity of the cell with the given index
        """
        return self.activities[self.neighbour_indices.index(cell_index)]

    def weight_from(self, cell_index):
        """
        Returns the connection weight of the cell with the given cell index to the current cell.
        :param cell_index: the index of the cell whose connection strength to the current cell is being requested
        :return: the connection strength of the cell with the given index to the current cell
        """
        return self.weights[self.neighbour_indices.index(cell_index)]

    def past_activity_of(self, cell_index, past_activity_index=-1):
        """
        Returns the activity of the cell with the given cell index, in the past.
        :param cell_index: the index of the cell whose activity is being requested
        :param past_activity_index: the index of the past activity (-1 means the timestep before the last timestep)
        :return: the activity of the cell with the given index, in the past
        """
        return self.past_activities[past_activity_index][self.neighbour_indices.index(cell_index)]

    @property
    def activities(self):
        """
        A list containing the neighbourhood's activities.
        :return: a list containing the neighbourhood's activities
        """
        return self._activities

    @property
    def neighbour_indices(self):
        """
        A list containing the neighbourhood's cell indices.
        :return: a list containing the neighbourhood's cell indices
        """
        return self._neighbour_indices

    @property
    def weights(self):
        """
        A list containing the weights of the connections to the cell.
        :return: a list containing the weights of the connections to the cell
        """
        return self._weights

    @property
    def current_activity(self):
        """
        The current activity of the cell.
        :return: the current activity of the cell
        """
        return self._current_activity

    @property
    def perturbation(self):
        return self._perturbation

    @property
    def past_activities(self):
        """
        A list of lists containing the past activities. The last entry in the list (with index -1) will contain
        the activities for the neighbourhood at the timestep before the last timestep, the second-to-last entry in the
        list (with index -2) will contain the activities before that, etc.
        :return: a list of lists containing the past activities
        """
        return self._past_activities


def evolve(initial_conditions, adjacency_matrix, activity_rule, timesteps=None, input=None, connectivity_rule=None,
           perturbation=None, past_conditions=None, parallel=False, processes=None):
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
    :param input: a list representing the inputs to the network at each timestep, or a function that accepts the
                  current timestep number, returns the input for that timestep, or None to signal the end of the
                  evolution; if a list is provided, each item in the list contains the input for each cell in the
                  network for a particular timestep; the activity_rule (and any perturbation) will receive the current
                  input value for a given cell instead of the current timestep number itself, when the input parameter
                  is provided; either the input or timesteps parameter must be provided, but not both; if the input
                  parameter is provided, it will override the timesteps parameter, and the timesteps parameter will
                  have no effect; the first item in the input list is given to the network at t=1, the second at t=2,
                  etc. (i.e. no input is specified for the initial state); specifying the input implies an automaton
                  whose evolution is driven by an external signal
    :param connectivity_rule: the rule that will determine the connectivity of the network
    :param perturbation: a function that defines a perturbation applied as the system evolves; the function accepts
                         three parameters: c, which represents the cell index, t, which represents the timestep, and a,
                         which represents the computed activity for the cell given by c. The function must return the
                         new activity for cell c at timestep t.
    :param past_conditions: a list of lists that represent activities of the network that existed before the initial
                           timestep; if this parameter is provided, then the Neighbourhood will contain past_activities;
                           there will be as many past_activities entries as there are entries in this list
    :param parallel: whether the evolution of the cells should be performed in parallel;
                     Note: the activity_rule function must be safe to use concurrently, as it will
                     be invoked concurrently from different processes when this flag is set to True (the same is true
                     for the perturbation function); this generally means that the activity rule (and perturbation)
                     function cannot keep any state; some built-in rules, such as AsynchronousRule, won't work correctly
                     when 'parallel' is True
    :param processes: the number of processes to start for parallel execution, if 'parallel' is set to True;
                      the number of CPUs will be used if 'processes' is not provided and 'parallel' is True
    :return: a tuple of the activities over time and the connectivities over time
    """
    if len(initial_conditions) != len(adjacency_matrix[0]):
        raise Exception("the length of the initial conditions list does not match the given adjacency matrix")

    input_fn, steps = _get_input_function(timesteps, input)

    if connectivity_rule is not None:
        return _evolve_both(initial_conditions, adjacency_matrix, activity_rule, steps, input_fn, connectivity_rule,
                            perturbation, past_conditions)
    else:
        if parallel:
            return _evolve_activities_parallel(initial_conditions, adjacency_matrix, activity_rule, steps, input_fn,
                                               perturbation, processes, past_conditions)
        else:
            return _evolve_activities(initial_conditions, adjacency_matrix, activity_rule, steps, input_fn,
                                      perturbation, past_conditions)


def _evolve_activities(initial_conditions, adjacency_matrix, activity_rule, steps, input_fn, perturbation,
                       past_conditions):

    activities_over_time = np.empty((steps, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
    activities_over_time[0] = initial_conditions

    num_cells = len(adjacency_matrix[0])
    connectivities_sparse = sparse.csc_matrix(adjacency_matrix)
    nonzero_index_map = {}
    weight_map = {}
    for c in range(num_cells):
        sparse_col =  connectivities_sparse.getcol(c)
        nonzero_index_map[c] = sparse_col.nonzero()[0].tolist()
        weight_map[c] = sparse_col.data.tolist()

    t = 1
    while True:
        inp = input_fn(t)
        if inp is None:
            break
        last_activities = activities_over_time[t - 1]
        past = _get_past_activities(past_conditions, activities_over_time, t)

        if t == len(activities_over_time):
            activities_over_time = _extend_activities(activities_over_time, initial_conditions)

        for c in range(num_cells):
            nonzero_indices = nonzero_index_map[c]
            activities = [last_activities[i] for i in nonzero_indices]
            past_activities = [[p[i] for i in nonzero_indices] for p in past] if past else None
            weights = weight_map[c]
            cell_in = inp[c] if _is_indexable(inp) else inp
            neighbourhood = Neighbourhood(activities, nonzero_indices, weights, last_activities[c],
                                          perturbation, past_activities)
            activities_over_time[t][c] = activity_rule(neighbourhood, c, cell_in)
            if perturbation is not None:
                activities_over_time[t][c] = perturbation(c, activities_over_time[t][c], cell_in)

        t += 1

    return activities_over_time, [adjacency_matrix]*steps


def _get_past_activities(past_conditions, activities_over_time, t):
    if past_conditions and len(past_conditions) > 0:
        past_activities = [None]*len(past_conditions)
        last_t = t - 1
        for i in range(len(past_conditions)-1, -1, -1):
            past_activities[i] = past_conditions[last_t-1] if last_t < 1 else activities_over_time[last_t-1]
            last_t -= 1
        return past_activities
    return None


def _get_input_function(timesteps=None, input=None):
    if timesteps is None and input is None:
        raise Exception("either the timesteps or input must be provided")

    if input is not None:
        if callable(input):
            return input, 1
        else:
            return _ListInputFunction(input), len(input)+1

    return _TimestepInputFunction(timesteps), timesteps


class _TimestepInputFunction:
    def __init__(self, num_steps):
        self._num_steps = num_steps

    def __call__(self, t):
        if t == self._num_steps:
            return None
        return t


class _ListInputFunction:
    def __init__(self, input_list):
        self._input_list = input_list

    def __call__(self, t):
        if (t-1) >= len(self._input_list):
            return None
        return self._input_list[t-1]


def _is_indexable(obj):
    return isinstance(obj, collections.Sequence)


def _extend_activities(activities_over_time, initial_conditions):
    arr = np.empty((1, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
    return np.append(activities_over_time, arr, axis=0)


def _extend_connectivities(connectivities_over_time, adjacency_matrix):
    arr = np.empty((1, len(adjacency_matrix), len(adjacency_matrix)), dtype=np.dtype(type(adjacency_matrix[0][0])))
    return np.append(connectivities_over_time, arr, axis=0)


def _process_cells(cell_indices, inp, last_activities, past):
    global nonzero_index_map
    global weight_map
    global fn_activity
    global fn_perturb
    results = {}
    for c in cell_indices:
        nonzero_indices = nonzero_index_map[c]
        activities = [last_activities[i] for i in nonzero_indices]
        past_activities = [[p[i] for i in nonzero_indices] for p in past] if past else None
        weights = weight_map[c]
        cell_in = inp[c] if _is_indexable(inp) else inp
        neighbourhood = Neighbourhood(activities, nonzero_indices, weights, last_activities[c],
                                      fn_perturb, past_activities)
        cell_activity = fn_activity(neighbourhood, c, cell_in)
        if fn_perturb is not None:
            cell_activity = fn_perturb(c, cell_activity, cell_in)
        results[c] = cell_activity
    return results


def _evolve_activities_parallel(initial_conditions, adjacency_matrix, activity_rule, steps, input_fn,
                                perturbation, processes, past_conditions):

    activities_over_time = np.empty((steps, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
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

    if processes is None:
        processes = multiprocessing.cpu_count()
    cell_index_chunks = np.array_split(np.array(range(num_cells)), processes)
    pool = Pool(processes=processes)

    t = 1
    while True:
        inp = input_fn(t)
        if inp is None:
            break
        last_activities = activities_over_time[t - 1]
        past = _get_past_activities(past_conditions, activities_over_time, t)

        if t == len(activities_over_time):
            activities_over_time = _extend_activities(activities_over_time, initial_conditions)

        args = [(chunk, inp, last_activities, past) for chunk in cell_index_chunks]
        map_result = pool.starmap_async(_process_cells, args)

        for results in map_result.get():
            for c in results.keys():
                activities_over_time[t][c] = results[c]

        t += 1

    pool.close()
    pool.join()

    return activities_over_time, [adjacency_matrix]*steps


def _evolve_both(initial_conditions, adjacency_matrix, activity_rule, steps, input_fn,
                 connectivity_rule=ConnectivityRule.noop, perturbation=None, past_conditions=None):

    activities_over_time = np.empty((steps, len(initial_conditions)), dtype=np.dtype(type(initial_conditions[0])))
    activities_over_time[0] = initial_conditions

    connectivities_over_time = np.empty((steps, len(adjacency_matrix), len(adjacency_matrix)), dtype=np.dtype(type(adjacency_matrix[0][0])))
    connectivities_over_time[0] = adjacency_matrix

    num_cells = len(adjacency_matrix[0])

    t = 1
    while True:
        inp = input_fn(t)
        if inp is None:
            break
        last_activities = activities_over_time[t - 1]
        past = _get_past_activities(past_conditions, activities_over_time, t)
        last_connectivities = connectivities_over_time[t - 1]

        if t == len(activities_over_time):
            activities_over_time = _extend_activities(activities_over_time, initial_conditions)

        if t == len(connectivities_over_time):
            connectivities_over_time = _extend_connectivities(connectivities_over_time, adjacency_matrix)

        last_connectivities_transposed = np.array(last_connectivities).T

        nonzeros = np.nonzero(last_connectivities_transposed)
        index_map = {i: [] for i in range(num_cells)}
        [index_map[idx].append(nonzeros[1][i]) for i, idx in enumerate(nonzeros[0])]

        for c in range(num_cells):
            # use the transpose of the adjacency matrix to get the cells that are inputs to a given cell defined by a row
            row = last_connectivities_transposed[c]
            nonzero_indices = index_map[c]
            activities = last_activities[nonzero_indices]
            past_activities = [[p[i] for i in nonzero_indices] for p in past] if past else None
            weights = row[nonzero_indices]
            cell_in = inp[c] if _is_indexable(inp) else inp
            neighbourhood = Neighbourhood(activities, nonzero_indices, weights, last_activities[c],
                                          perturbation, past_activities)
            activities_over_time[t][c] = activity_rule(neighbourhood, c, cell_in)
            if perturbation is not None:
                activities_over_time[t][c] = perturbation(c, activities_over_time[t][c], cell_in)

        connectivities = connectivity_rule(last_connectivities, last_activities, t)
        connectivities_over_time[t] = connectivities

        t += 1

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
