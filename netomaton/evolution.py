import collections
import gc
from enum import Enum

import msgpack
import numpy as np
import scipy.sparse as sparse


class NodeContext(object):
    """
    The NodeContext consists of the states, identities (as node indices), and adjancency matrix weights of the nodes
    that influence a given node. Each of the properties (i.e. activities, neighbour_indices, connection states) are
    represented as lists. Each of the lists are of the same size, and the first item in each list corresponds to the
    first node in the neighbourhood, etc. The neighbourhood of a node also contains the node's current activity (i.e.
    the activity as of the last timestep).
    """

    __slots__ = ("node_label", "timestep", "activities", "neighbour_labels", "neighbourhood_activities",
                 "connection_states", "current_activity", "past_activities", "input", "added_nodes", "removed_nodes")

    def __init__(self, node_label, timestep, activities, neighbour_labels, neighbourhood_activities, connection_states,
                 current_activity, past_activities, input):
        """
        :param node_label: the label of the node being processed
        :param timestep: the current timestep
        :param activities: the activities of all the nodes after the previous timestep
        :param neighbour_labels: the labels of all neighbour nodes
        :param neighbourhood_activities: the node states of all neighbourhood nodes
        :param connection_states: the states of all the incoming connections of the node being processed
        :param current_activity: the state of the node after the previous timestep
        :param past_activities: the past activities of previous timesteps for all nodes
        :param input: the input for this timestep, if provided, or None otherwise
        """
        self.node_label = node_label
        self.timestep = timestep
        self.activities = activities
        self.neighbour_labels = neighbour_labels
        self.neighbourhood_activities = neighbourhood_activities
        self.connection_states = connection_states
        self.current_activity = current_activity
        self.past_activities = past_activities
        self.input = input
        self.added_nodes = []
        self.removed_nodes = []

    def activity_of(self, node_label):
        return self.activities[node_label]

    # TODO support incoming_links also; must provide one or the other
    def add_node(self, state, outgoing_links, nodel_label):
        self.added_nodes.append((state, outgoing_links, nodel_label))

    def remove_node(self, nodel_label):
        self.removed_nodes.append(nodel_label)

    def past_activity_of(self, node_label, past_activity_index=-1):
        """
        Returns the activity of the node with the given node label, in the past.
        :param node_label: the label of the node whose activity is being requested
        :param past_activity_index: the index of the past activity (-1 means the timestep before the last timestep)
        :return: the activity of the node with the given label, in the past
        """
        return self.past_activities[past_activity_index][node_label]


class ConnectivityContext(object):

    __slots__ = ("_connectivity_map", "_activities", "_timestep")

    def __init__(self, connectivity_map, activities, t):
        self._connectivity_map = connectivity_map
        self._activities = activities
        self._timestep = t

    @property
    def connectivity_map(self):
        return self._connectivity_map

    @property
    def activities(self):
        return self._activities

    @property
    def timestep(self):
        return self._timestep


class PerturbationContext(object):
    """
    The PerturbationContext contains the node label, activity and input for a particular timestep.
    """

    __slots__ = ("_node_label", "_node_activity", "_timestep", "_input")

    def __init__(self, node_label, node_activity, timestep, input):
        self._node_label = node_label
        self._node_activity = node_activity
        self._timestep = timestep
        self._input = input

    @property
    def node_label(self):
        return self._node_label

    @property
    def node_activity(self):
        return self._node_activity

    @property
    def timestep(self):
        return self._timestep

    @property
    def input(self):
        return self._input


class UpdateOrder(Enum):
    ACTIVITIES_FIRST = 1
    TOPOLOGY_FIRST = 2
    SYNCHRONOUS = 3


# TODO rename "connectivity" everywhere; to "topology" perhaps? as in "topological table"
def evolve(topology, initial_conditions=None, activity_rule=None, timesteps=None, input=None, connectivity_rule=None,
           perturbation=None, past_conditions=None, update_order=UpdateOrder.ACTIVITIES_FIRST, copy_connectivity=True,
           compression=False):

    if initial_conditions is None:
        initial_conditions = {}

    # convert initial_conditions to map, if it isn't already
    if not isinstance(initial_conditions, dict) and isinstance(initial_conditions, (list, np.ndarray)):
        initial_conditions = {i: check_np(v) for i, v in enumerate(initial_conditions)}

    # key is the timestep; value is a map of the network activities,
    #   where the key is the node label, and value is the activity
    activities_over_time = {0: Activities(initial_conditions, compression)}
    input_fn, steps = _get_input_function(timesteps, input)

    connectivity_map, was_adjacency_matrix = _get_connectivity_map(topology)

    if len(initial_conditions) != len(connectivity_map) and activity_rule:
        raise Exception("too few intial conditions specified [%s] for the number of given nodes [%s]" %
                        (len(initial_conditions), len(connectivity_map)))

    connectivities_over_time = {0: Topology(connectivity_map, compression)}

    prev_activities = initial_conditions
    prev_connectivities = connectivity_map

    t = 1
    while True:
        inp = input_fn(t)
        if inp is None:
            break

        past = _get_past_activities(past_conditions, activities_over_time, t)
        curr_activities = {}

        if update_order is UpdateOrder.ACTIVITIES_FIRST:
            added_nodes, removed_nodes = evolve_activities(activity_rule, t, inp, curr_activities, prev_activities,
                                                           activities_over_time, prev_connectivities, past,
                                                           perturbation, compression)
            curr_connectivities = evolve_topology(connectivity_rule, t, curr_activities, prev_connectivities,
                                                  connectivities_over_time, copy_connectivity, compression,
                                                  added_nodes, removed_nodes)

        elif update_order is UpdateOrder.TOPOLOGY_FIRST:
            curr_connectivities = evolve_topology(connectivity_rule, t, prev_activities, prev_connectivities,
                                                  connectivities_over_time, copy_connectivity, compression)
            # added and removed nodes are ignore in this case
            evolve_activities(activity_rule, t, inp, curr_activities, prev_activities,
                              activities_over_time, curr_connectivities, past, perturbation, compression)

        elif update_order is UpdateOrder.SYNCHRONOUS:
            # TODO create test
            curr_connectivities = evolve_topology(connectivity_rule, t, prev_activities, prev_connectivities,
                                                  connectivities_over_time, copy_connectivity, compression)
            # added and removed nodes are ignore in this case
            evolve_activities(activity_rule, t, inp, curr_activities, prev_activities,
                              activities_over_time, prev_connectivities, past, perturbation, compression)

        else:
            raise Exception("unsupported update_order: %s" % update_order)

        prev_activities = curr_activities
        prev_connectivities = curr_connectivities

        t += 1

    if was_adjacency_matrix:
        if activity_rule:
            activities_over_time = convert_activities_map_to_list(activities_over_time)
        if connectivity_rule:
            connectivities_over_time = convert_connectivities_map_to_list(connectivities_over_time)

    return activities_over_time, connectivities_over_time


def evolve_activities(activity_rule, t, inp, curr_activities, prev_activities, activities_over_time, connectivity_map,
                      past, perturbation, compression):
    added_nodes = []
    removed_nodes = []
    if activity_rule:
        added_nodes, removed_nodes = do_activity_rule(t, inp, curr_activities, prev_activities, connectivity_map,
                                                      activity_rule, past, perturbation)

        if added_nodes:
            for state, outgoing_links, node_label in added_nodes:
                curr_activities[node_label] = state

    activities_over_time[t] = Activities(curr_activities, compression)

    return added_nodes, removed_nodes


def do_activity_rule(t, inp, curr_activities, prev_activities, connectivity_map, activity_rule, past, perturbation):
    added_nodes = []
    removed_nodes = []

    for node_label, incoming_connections in connectivity_map.items():
        neighbour_labels = [k for k in incoming_connections]
        current_activity = prev_activities[node_label]
        neighbourhood_activities = [prev_activities[neighbour_label] for neighbour_label in neighbour_labels]
        node_in = None if inp == "__timestep__" else inp[node_label] if _is_indexable(inp) else inp
        ctx = NodeContext(node_label, t, prev_activities, neighbour_labels, neighbourhood_activities,
                          incoming_connections, current_activity, past, node_in)

        new_activity = activity_rule(ctx)
        new_activity = check_np(new_activity)

        if ctx.added_nodes:
            added_nodes.extend(ctx.added_nodes)
        if ctx.removed_nodes:
            removed_nodes.extend(ctx.removed_nodes)

        if node_label not in ctx.removed_nodes:
            curr_activities[node_label] = new_activity

        if perturbation is not None:
            pctx = PerturbationContext(node_label, curr_activities[node_label], t, node_in)
            curr_activities[node_label] = perturbation(pctx)

    return added_nodes, removed_nodes


def evolve_topology(connectivity_rule, t, activities, prev_connectivities, connectivities_over_time, copy_connectivity,
                    compression, added_nodes=None, removed_nodes=None):
    connectivity_map = prev_connectivities
    if added_nodes or removed_nodes:
        connectivity_map = copy_connectivity_map(connectivity_map)

        # adjust connectivity map according to node deletions and insertions
        for node_label in removed_nodes:
            del connectivity_map[node_label]

        for state, outgoing_links, node_label in added_nodes:
            connectivity_map[node_label] = {}
            for target, connection_state in outgoing_links.items():
                connectivity_map[target][node_label] = connection_state

    if connectivity_rule:
        if copy_connectivity:
            connectivity_map = copy_connectivity_map(connectivity_map)
        connectivity_map = connectivity_rule(ConnectivityContext(connectivity_map, activities, t))
        if not connectivity_map:
            raise Exception("connectivity rule must return a connectivity map")

    connectivities_over_time[t] = Topology(connectivity_map, compression)

    return connectivity_map


def copy_connectivity_map(conn_map):
    return _CompressedDict(conn_map, True).to_dict()


def convert_activities_map_to_list(activities_map_over_time):
    activities_over_time = []
    for i in activities_map_over_time:
        activities = activities_map_over_time[i].to_dict()
        activities_list = []
        for c in sorted(activities):  #TODO do we need to sort?
            activities_list.append(activities[c])
        activities_over_time.append(activities_list)
    return activities_over_time


def convert_connectivities_map_to_list(connectivities_map_over_time):
    connectivities_over_time = []
    for i in connectivities_map_over_time:
        connectivities = connectivities_map_over_time[i].to_dict()
        num_nodes = len(connectivities)
        adjacency_matrix = [[0. for _ in range(num_nodes)] for _ in range(num_nodes)]
        for c in sorted(connectivities):  #TODO do we need to sort?
            for n in sorted(connectivities[c]):  #TODO do we need to sort?
                adjacency_matrix[n][c] = connectivities[c][n]["weight"] if "weight" in connectivities[c][n] else 1.0
        connectivities_over_time.append(adjacency_matrix)
    return connectivities_over_time


def _get_connectivity_map(topology):
    """
    :param topology: the topology specifying the underlying network
    :return: a connectivity map and whether or not an adjacency matrix was provided
    """
    if isinstance(topology, (list, np.ndarray)):
        # assume we have an adjacency matrix
        return _convert_adjacency_matrix_to_connectivity_map(topology), True
    elif isinstance(topology, dict):
        # assume we have a connectivity map
        return topology, False
    raise Exception("only an adjancency matrix and connectivity map are supported as network representations")


def _convert_adjacency_matrix_to_connectivity_map(adjacency_matrix):
    # since we require Python 3.6, and dicts respect insertion order, we're using a plain dict here
    # (even though the 3.6 language spec doesn't officially support it)
    connectivity_map = {}

    num_nodes = len(adjacency_matrix[0])
    adjacencies_sparse = sparse.csc_matrix(adjacency_matrix)
    nonzero_index_map = {}
    weight_map = {}
    for c in range(num_nodes):
        sparse_col = adjacencies_sparse.getcol(c)
        nonzero_index_map[c] = sparse_col.nonzero()[0].tolist()
        weight_map[c] = sparse_col.data.tolist()

    for n in range(num_nodes):
        connectivity_map[n] = {}
        nonzero_indices = nonzero_index_map[n]
        for i, neighbour_index in enumerate(nonzero_indices):
            connectivity_map[n][neighbour_index] = [{"weight": weight_map[n][i]}]

    return connectivity_map


def _get_past_activities(past_conditions, activities_over_time, t):
    if past_conditions and len(past_conditions) > 0:
        past_activities = [None]*len(past_conditions)
        last_t = t - 1
        for i in range(len(past_conditions)-1, -1, -1):

            curr_past_cond = past_conditions[last_t-1] if last_t < 1 else activities_over_time[last_t-1].to_dict()
            if not isinstance(curr_past_cond, dict) and isinstance(curr_past_cond, (list, np.ndarray)):
                curr_past_cond = {i: v for i, v in enumerate(curr_past_cond)}

            past_activities[i] = curr_past_cond
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


def _is_indexable(obj):
    return isinstance(obj, collections.Sequence)


class _TimestepInputFunction:
    def __init__(self, num_steps):
        self._num_steps = num_steps

    def __call__(self, t):
        if t == self._num_steps:
            return None
        return "__timestep__"


class _ListInputFunction:
    def __init__(self, input_list):
        self._input_list = input_list

    def __call__(self, t):
        if (t-1) >= len(self._input_list):
            return None
        return self._input_list[t-1]


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
    :param k: the number of states in the Network Automaton (2, by default)
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


class _CompressedDict:
    __slots__ = ("_map", "_compression")

    def __init__(self, m, compression):
        self._compression = compression
        self._map = self._compress(m) if compression else m

    def to_dict(self):
        return self._decompress(self._map) if self._compression else self._map

    def _compress(self, d):
        return msgpack.packb(d)

    def _decompress(self, b):
        gc.disable()
        d = msgpack.unpackb(b, strict_map_key=False)
        gc.enable()
        return d


class Topology(_CompressedDict):
    def __init__(self, connectivity_map, compression):
        super().__init__(connectivity_map, compression)


class Activities(_CompressedDict):
    def __init__(self, activities, compression):
        super().__init__(activities, compression)


def check_np(obj):
    if isinstance(obj, np.generic):
        return np.asscalar(obj)
    return obj
