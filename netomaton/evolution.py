import numpy as np
import scipy.sparse as sparse
import collections


class NodeContext(object):
    """
    The NodeContext consists of the states, identities (as node indices), and adjancency matrix weights of the nodes
    that influence a given node. Each of the properties (i.e. activities, neighbour_indices, connection states) are
    represented as lists. Each of the lists are of the same size, and the first item in each list corresponds to the
    first node in the neighbourhood, etc. The neighbourhood of a node also contains the node's current activity (i.e.
    the activity as of the last timestep).
    """
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

# TODO rename "connectivity" everywhere; to "topology" perhaps?
def evolve(topology, initial_conditions=None, activity_rule=None, timesteps=None, input=None, connectivity_rule=None,
           perturbation=None, past_conditions=None):

    if initial_conditions is None:
        initial_conditions = {}

    # convert initial_conditions to map, if it isn't already
    if not isinstance(initial_conditions, dict) and isinstance(initial_conditions, (list, np.ndarray)):
        initial_conditions = {i: v for i, v in enumerate(initial_conditions)}

    # key is the timestep; value is a map of the network activities,
    #   where the key is the node label, and value is the activity
    activities_over_time = {0: initial_conditions}  #TODO should the first timestep start at 1?
    input_fn, steps = _get_input_function(timesteps, input)

    connectivity_map, was_adjacency_matrix = _get_connectivity_map(topology)

    if len(initial_conditions) != len(connectivity_map) and activity_rule:
        raise Exception("too few intial conditions specified [%s] for the number of given nodes [%s]" %
                        (len(initial_conditions), len(connectivity_map)))

    connectivities_over_time = {0: copy_connectivity_map(connectivity_map)}

    t = 1
    while True:
        inp = input_fn(t)
        if inp is None:
            break

        past = _get_past_activities(past_conditions, activities_over_time, t)
        activities_over_time[t] = {}
        connectivities_over_time[t] = {}

        if activity_rule:
            added_nodes, removed_nodes = do_activity_rule(t, inp, activities_over_time, connectivity_map,
                                                          activity_rule, past, perturbation)

            # adjust connectivity map according to node deletions and insertions
            for node_label in removed_nodes:
                del connectivity_map[node_label]

            for state, outgoing_links, node_label in added_nodes:
                connectivity_map[node_label] = {}
                for target, connection_state in outgoing_links.items():
                    connectivity_map[target][node_label] = connection_state

                activities_over_time[t][node_label] = state

            if added_nodes or removed_nodes:
                connectivities_over_time[t] = copy_connectivity_map(connectivity_map)

        if connectivity_rule:
            # TODO we should support the option to have the connectivity rule executed before the activity rule
            # TODO we need a demo that uses the connectivity rule before the activity rule
            # the connectivity rule receives any changes made to the network via the activity rule
            connectivity_map = connectivity_rule(ConnectivityContext(connectivity_map, activities_over_time[t], t))
            connectivities_over_time[t] = copy_connectivity_map(connectivity_map)

        t += 1

    if was_adjacency_matrix:
        if activity_rule:
            activities_over_time = _convert_activities_map_to_list(activities_over_time)
        if connectivity_rule:
            connectivities_over_time = _convert_connectivities_map_to_list(connectivities_over_time)

    return activities_over_time, connectivities_over_time


def do_activity_rule(t, inp, activities_over_time, connectivity_map, activity_rule, past, perturbation):
    added_nodes = []
    removed_nodes = []

    last_activities = activities_over_time[t - 1]

    for node_label, incoming_connections in connectivity_map.items():
        neighbour_labels = [k for k in incoming_connections]
        current_activity = last_activities[node_label]
        neighbourhood_activities = [last_activities[neighbour_label] for neighbour_label in neighbour_labels]
        node_in = None if inp == "__timestep__" else inp[node_label] if _is_indexable(inp) else inp
        ctx = NodeContext(node_label, t, last_activities, neighbour_labels, neighbourhood_activities,
                          incoming_connections, current_activity, past, node_in)

        new_activity = activity_rule(ctx)

        if ctx.added_nodes:
            added_nodes.extend(ctx.added_nodes)
        if ctx.removed_nodes:
            removed_nodes.extend(ctx.removed_nodes)

        if node_label not in ctx.removed_nodes:
            activities_over_time[t][node_label] = new_activity

        if perturbation is not None:
            pctx = PerturbationContext(node_label, activities_over_time[t][node_label], t, node_in)
            activities_over_time[t][node_label] = perturbation(pctx)

    return added_nodes, removed_nodes


def copy_connectivity_map(conn_map):
    new_map = type(conn_map)()
    for k1, v1 in conn_map.items():
        new_links = type(v1)()
        for k2, v2 in v1.items():
            new_links[k2] = _deep_copy_value(v2)
        new_map[k1] = new_links
    return new_map


def _deep_copy_value(val):
    if isinstance(val, (list, tuple)):
        new_val = []
        for v in val:
            new_val.append(_deep_copy_value(v))
        val = tuple(new_val) if isinstance(val, tuple) else new_val
    elif isinstance(val, (dict, collections.OrderedDict)):
        new_val = type(val)()
        for k, v in val.items():
            new_val[k] = _deep_copy_value(v)
        val = new_val
    return val


def _convert_activities_map_to_list(activities_map_over_time):
    activities_over_time = []
    for timestep in sorted(activities_map_over_time):  #TODO do we need to sort?
        activities = activities_map_over_time[timestep]
        activities_list = []
        for c in sorted(activities):  #TODO do we need to sort?
            activities_list.append(activities[c])
        activities_over_time.append(activities_list)
    return activities_over_time


def _convert_connectivities_map_to_list(connectivities_map_over_time):
    connectivities_over_time = []
    for timestep in sorted(connectivities_map_over_time):  #TODO do we need to sort?
        connectivities = connectivities_map_over_time[timestep]
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

            curr_past_cond = past_conditions[last_t-1] if last_t < 1 else activities_over_time[last_t-1]
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
