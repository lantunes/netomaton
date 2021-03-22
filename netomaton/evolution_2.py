import numpy as np
import scipy.sparse as sparse
import collections


class NodeContext_2(object):
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
        :param activities: the activities of all the nodes after the previous timestep #TODO change "activity" to "node state"
        :param neighbour_labels: the labels of all neighbour nodes
        :param neighbourhood_activities: the node states of all neighbourhood nodes
        :param connection_states: the states of all the incoming connections of the node being processed
        :param current_activity: the state of the node after the previous timestep
        :param past_activities: #TODO
        :param input: #TODO
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
    def add_node(self, state, outgoing_links, nodel_label=None):
        self.added_nodes.append((state, outgoing_links, nodel_label))

    def remove_node(self, nodel_label):
        self.removed_nodes.append(nodel_label)


class ConnectivityContext_2(object):
    def __init__(self, connectivities, activities, t):
        self._connectivities = connectivities
        self._activities = activities
        self._timestep = t

    @property
    def connectivities(self):
        return self._connectivities

    @property
    def activities(self):
        return self._activities

    @property
    def timestep(self):
        return self._timestep


def evolve_2(initial_conditions, topology, activity_rule, timesteps=None, input=None, connectivity_rule=None,
             perturbation=None, past_conditions=None, parallel=False, processes=None):

    # convert initial_conditions to map, if it isn't already
    if not isinstance(initial_conditions, dict) and isinstance(initial_conditions, (list, np.ndarray)):
        initial_conditions = {i: v for i, v in enumerate(initial_conditions)}

    # key is the timestep; value is a map of the network activities,
    #   where the key is the node label, and value is the activity
    activities_over_time = {0: initial_conditions}  #TODO should the first timestep start at 1?
    input_fn, steps = _get_input_function(timesteps, input)

    connectivity_map, was_adjacency_matrix = _get_connectivity_map(topology)

    if len(initial_conditions) != len(connectivity_map):
        raise Exception("too few intial conditions specified [%s] for the number of given nodes [%s]" %
                        (len(initial_conditions), len(connectivity_map)))

    connectivities_over_time = {}
    if connectivity_rule:
        connectivities_over_time[0] = copy_connectivity_map(connectivity_map)

    last_node_index = len(connectivity_map) - 1

    t = 1
    while True:
        inp = input_fn(t)
        if inp is None:
            break

        last_activities = activities_over_time[t - 1]
        # past = _get_past_activities(past_conditions, activities_over_time, t) # TODO
        activities_over_time[t] = {}

        # if t == len(activities_over_time): # TODO
        #     activities_over_time = _extend_activities(activities_over_time, initial_conditions)

        added_nodes = []
        removed_nodes = []

        for node_label in connectivity_map:
            neighbour_labels = [k for k in connectivity_map[node_label]]
            current_activity = last_activities[node_label]
            neighbourhood_activities = [last_activities[neighbour_label] for neighbour_label in neighbour_labels]
            past_activities = None
            node_in = None if inp == "__timestep__" else inp[node_label] if _is_indexable(inp) else inp
            ctx = NodeContext_2(node_label, t, last_activities, neighbour_labels, neighbourhood_activities,
                                connectivity_map[node_label], current_activity, past_activities, node_in)

            new_activity = activity_rule(ctx)

            added_nodes.extend(ctx.added_nodes)
            removed_nodes.extend(ctx.removed_nodes)

            if node_label not in ctx.removed_nodes:
                activities_over_time[t][node_label] = new_activity

        # adjust connectivity map according to node deletions and insertions
        for node_label in removed_nodes:
            del connectivity_map[node_label]

        for state, outgoing_links, node_label in added_nodes:
            if node_label is None:
                last_node_index += 1
                node_label = last_node_index
            connectivity_map[node_label] = {}
            for target, weight in outgoing_links.items():
                connectivity_map[target][node_label] = weight

            activities_over_time[t][node_label] = state

        if connectivity_rule:
            # TODO we should support the option to have the connectivity rule executed before the activity rule
            # the connectivity rule receives any changes made to the network via the activity rule
            connectivity_map = connectivity_rule(ConnectivityContext_2(connectivity_map, activities_over_time[t], t))
            connectivities_over_time[t] = copy_connectivity_map(connectivity_map)

        t += 1

    if was_adjacency_matrix:
        activities_over_time = _convert_activities_map_to_list(activities_over_time)
        if connectivity_rule:
            connectivities_over_time = _convert_connectivities_map_to_list(connectivities_over_time)

    return activities_over_time, connectivities_over_time


def copy_connectivity_map(conn_map):
    new_map = type(conn_map)()
    for k1, v1 in conn_map.items():
        new_links = type(v1)()
        for k2, v2 in v1.items():
            new_links[k2] = v2
        new_map[k1] = new_links
    return new_map


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
                adjacency_matrix[n][c] = connectivities[c][n]
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
            connectivity_map[n][neighbour_index] = weight_map[n][i]

    return connectivity_map


def _get_input_function(timesteps=None, input=None):
    if timesteps is None and input is None:
        raise Exception("either the timesteps or input must be provided")

    if input is not None:
        if callable(input):
            return input, 1
        else:
            return _ListInputFunction_2(input), len(input)+1

    return _TimestepInputFunction_2(timesteps), timesteps


def _is_indexable(obj):
    return isinstance(obj, collections.Sequence)


class _TimestepInputFunction_2:
    def __init__(self, num_steps):
        self._num_steps = num_steps

    def __call__(self, t):
        if t == self._num_steps:
            return None
        return "__timestep__"


class _ListInputFunction_2:
    def __init__(self, input_list):
        self._input_list = input_list

    def __call__(self, t):
        if (t-1) >= len(self._input_list):
            return None
        return self._input_list[t-1]
