import collections
from enum import Enum
from .state import State

import numpy as np


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

    def edge_data(self, neigbour_label, attr, index=0):
        return self.connection_states[neigbour_label][index][attr]


class TopologyContext(object):
    """
    The TopologyContext contains the network and its activities for a particular timestep.
    """

    __slots__ = ("network", "activities", "timestep")

    def __init__(self, network, activities, t):
        self.network = network
        self.activities = activities
        self.timestep = t


class PerturbationContext(object):
    """
    The PerturbationContext contains the node label, activity and input for a particular timestep.
    """

    __slots__ = ("node_label", "node_activity", "timestep", "input")

    def __init__(self, node_label, node_activity, timestep, input):
        self.node_label = node_label
        self.node_activity = node_activity
        self.timestep = timestep
        self.input = input


class UpdateOrder(Enum):
    ACTIVITIES_FIRST = 1
    TOPOLOGY_FIRST = 2
    SYNCHRONOUS = 3


def evolve(network, initial_conditions=None, activity_rule=None, timesteps=None, input=None, topology_rule=None,
           perturbation=None, past_conditions=None, update_order=UpdateOrder.ACTIVITIES_FIRST, copy_network=True,
           compression=False, persist_activities=True, persist_network=True, memoize=False, memoization_key=None):
    """
    Evolves the given network with the given initial conditions, for the specified number of timesteps, using the given
    activity and topology rules. Note that if A(t) is the network at timestep t, and S(t) is the network activity vector
    at timestep t, and F is a function defining a topology rule, and G is a function describing an activity rule, then
    A(t+1) and S(t+1) are defined as follows:
    When `update_order` is `UpdateOrder.ACTIVITIES_FIRST`:
    S(t + 1) = G(A(t), S(t))
    A(t + 1) = F(A(t), S(t + 1))
    When `update_order` is `UpdateOrder.TOPOLOGY_FIRST`:
    A(t + 1) = F(A(t), S(t))
    S(t + 1) = G(A(t + 1), S(t))
    When`update_order` is `UpdateOrder.SYNCHRONOUS`:
    A(t + 1) = F(A(t), S(t))
    S(t + 1) = G(A(t), S(t))
    :param initial_conditions: the initial activities of the network
    :param network: the network defining the topology of the system
    :param activity_rule: the rule that will determine the activity of a node in the network
    :param timesteps: the number of steps in the evolution of the network; Note that the initial state, specified by the
                      initial_conditions, is considered the result of a timestep, so that the activity_rule is invoked
                      t - 1 times; for example, if timesteps is 6, then the initial state is considered the result of
                      the first timestep (t=0), and the activity_rule will be invoked five times; the activity_rule
                      (and any perturbation) will receive the current timestep number each time it is invoked;
                      specifying the timesteps implies an automaton that evolves on its own, in the absence of any
                      external driving signal
    :param input: a list representing the inputs to the network at each timestep, or a function that accepts the
                  current timestep number, returns the input for that timestep, or None to signal the end of the
                  evolution; if a list is provided, each item in the list contains the input for each node in the
                  network for a particular timestep; the activity_rule (and any perturbation) will receive the current
                  input value for a given node through the NodeContext, when the input parameter is provided;
                  either the input or timesteps parameter must be provided, but not both; if the input parameter is
                  provided, it will override the timesteps parameter, and the timesteps parameter will have no effect;
                  the first item in the input list is given to the network at t=1, the second at t=2, etc. (i.e. no
                  input is specified for the initial state); specifying the input implies an automaton whose evolution
                  is driven by an external signal
    :param topology_rule: the rule that will determine the topology of the network
    :param perturbation: a function that defines a perturbation applied as the system evolves; the function accepts
                         one parameter: the PerturbationContext. It contains the node index, the timestep, the computed
                         activity for the node, and its input (or None if there is no input). The function must return
                         the new activity for the node at the timestep.
    :param past_conditions: a list of lists that represent activities of the network that existed before the initial
                           timestep; if this parameter is provided, then the NodeContext will contain past_activities;
                           there will be as many past_activities entries as there are entries in this list
    :param update_order: the order in which to perform the update to the system (default is
                         `UpdateOrder.ACTIVITIES_FIRST`)
    :param copy_network: whether to copy the network during its evolution (default is True)
    :param compression: whether to compress the network when it is persisted in the State (default is False)
    :param persist_activities: whether to persist the activities in the State (default is True)
    :param persist_network: whether to persist the network in the State (default is True)
    :param memoize: whether to use memoization during evolution; if True, then the result of applying the rule for a
                    a given input will be cached, and used on subsequent invocations of the rule; this can result
                    in a significant improvement to execution speed if the rule is expensive to invoke; NOTE: this
                    should only be set to True for rules which do not store any state upon invocation (default is False)
    :param memoization_key: a user-specified key for memoization; by default, an appropriate memoization key is
                            used depending on the presence or absence of a rotation system on the network;
                            must be a `MemoizationKey` instance; this argument is relevant only when `memoize` is `True`
                            (default is None)
    :return: a trajectory, which is a list of States, where each State defines the network and its activities for a
             particular timestep
    """
    if initial_conditions is None:
        initial_conditions = {}

    # convert initial_conditions to map, if it isn't already
    if not isinstance(initial_conditions, dict) and isinstance(initial_conditions, (list, np.ndarray)):
        initial_conditions = {i: check_np(v) for i, v in enumerate(initial_conditions)}

    input_fn = _get_input_function(timesteps, input)

    if len(initial_conditions) != len(network) and activity_rule:
        raise Exception("too few intial conditions specified [%s] for the number of given nodes [%s]" %
                        (len(initial_conditions), len(network)))

    # key is the timestep
    trajectory = {0: State(activities=initial_conditions, network=network, compression=compression)}

    prev_activities = initial_conditions
    prev_network = network

    memo_table = {}
    if memoize and memoization_key is None:
        memoization_key = _UnorderedMemoizationKey() if network.rotation_system is None else _OrderedMemoizationKey()

    # create a neighbourhood map for efficiency if the network never changes (i.e. no topology rule)
    neighbourhood_map = None
    if topology_rule is None:
        neighbourhood_map = _get_neighbourhood_map(network)

    t = 1
    while True:
        inp = input_fn(t, prev_activities, prev_network)
        if inp is None:
            break

        past = _get_past_activities(past_conditions, trajectory, t)
        curr_activities = {}
        trajectory[t] = State(compression=compression)

        if update_order is UpdateOrder.ACTIVITIES_FIRST:
            added_nodes, removed_nodes = evolve_activities(activity_rule, t, inp, curr_activities, prev_activities,
                                                           trajectory, prev_network, past, perturbation, persist_activities,
                                                           memoize, memo_table, neighbourhood_map, memoization_key)
            curr_network = evolve_topology(topology_rule, t, curr_activities, prev_network,
                                           trajectory, copy_network, persist_network, added_nodes, removed_nodes)
            if added_nodes or removed_nodes:
                # re-build the neighbourhood map, since the network has changed
                neighbourhood_map = _get_neighbourhood_map(curr_network)

        elif update_order is UpdateOrder.TOPOLOGY_FIRST:
            curr_network = evolve_topology(topology_rule, t, prev_activities, prev_network,
                                           trajectory, copy_network, persist_network)
            # added and removed nodes are ignore in this case
            evolve_activities(activity_rule, t, inp, curr_activities, prev_activities, trajectory, curr_network, past,
                              perturbation, persist_activities, memoize, memo_table, neighbourhood_map, memoization_key)

        elif update_order is UpdateOrder.SYNCHRONOUS:
            # TODO create test
            curr_network = evolve_topology(topology_rule, t, prev_activities, prev_network,
                                           trajectory, copy_network, persist_network)
            # added and removed nodes are ignore in this case
            evolve_activities(activity_rule, t, inp, curr_activities, prev_activities, trajectory, prev_network, past,
                              perturbation, persist_activities, memoize, memo_table, neighbourhood_map, memoization_key)

        else:
            raise Exception("unsupported update_order: %s" % update_order)

        prev_activities = curr_activities
        prev_network = curr_network

        t += 1

    # since we require Python 3.6, and dicts respect insertion order, we don't sort the trajectory entries by key
    # (even though the 3.6 language spec doesn't officially support it)
    return list(trajectory.values())


def evolve_activities(activity_rule, t, inp, curr_activities, prev_activities, trajectory, network,
                      past, perturbation, persist_activities, memoize, memoization_table, neighbourhood_map,
                      memoization_key):
    added_nodes = []
    removed_nodes = []
    if activity_rule:
        added_nodes, removed_nodes = do_activity_rule(t, inp, curr_activities, prev_activities, network,
                                                      activity_rule, past, perturbation, memoize, memoization_table,
                                                      neighbourhood_map, memoization_key)

        if added_nodes:
            for state, outgoing_links, node_label in added_nodes:
                curr_activities[node_label] = check_np(state)

    if persist_activities:
        trajectory[t].activities = curr_activities

    return added_nodes, removed_nodes


def do_activity_rule(t, inp, curr_activities, prev_activities, network, activity_rule, past, perturbation,
                     memoize, memoization_table, neigh_map, memoization_key):
    added_nodes = []
    removed_nodes = []

    for node_label in network.nodes:
        incoming_connections = network.in_edges(node_label)
        neighbour_labels = _get_neighbour_labels(node_label, neigh_map, network, incoming_connections)
        current_activity = prev_activities[node_label]
        neighbourhood_activities = [prev_activities[neighbour_label] for neighbour_label in neighbour_labels]
        node_in = None if inp == "__timestep__" else inp[node_label] if _is_indexable(inp) else inp
        ctx = NodeContext(node_label, t, prev_activities, neighbour_labels, neighbourhood_activities,
                          incoming_connections, current_activity, past, node_in)

        if memoize:
            new_activity = _get_memoized(activity_rule, ctx, memoization_table, memoization_key)
        else:
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


def _get_neighbour_labels(node_label, neighbourhood_map, network, incoming_connections):
    if neighbourhood_map is not None:
        return neighbourhood_map[node_label]
    elif network.rotation_system is not None:
        return network.rotation_system[node_label]
    else:
        return [i for i in incoming_connections]


def _get_memoized(activity_rule, ctx, memoization_table, memoization_key):
    key = memoization_key.to_key(ctx)
    if key in memoization_table:
        return memoization_table[key]
    else:
        result = activity_rule(ctx)
        result = check_np(result)
        memoization_table[key] = result
        return result


class MemoizationKey:
    def to_key(self, ctx):
        pass


class _OrderedMemoizationKey(MemoizationKey):
    """
    An implementation of a memoization key that simply converts the context's neighbourhood activities into
    a tuple. This assumes that the ordering of the nodes in the neighbourhood matters, and that the ordering has
    been specified, such as by setting a Rotation System on the network. For example, a CTRBL rule, or an ECA rule,
    would require a Rotation System on the network.

    Note that this implementation doesn't include the current node if it isn't in its neighbourhood. If the rule
    depends on the current node, but the current node isn't in its neighbourhood, then the user should supply their
    own memoization key that adds the current node's activity. If the rule doesn't depend on the current node's
    activity, then we'd be adding cache entries unnecessarily if we added the current node to the key.
    e.g. [1,0,2], [1,3,2], [1,5,2], etc. all map to 9, so all we really need is a cache entry with [1,2]->9, but
    instead we'd end up adding the entries [0,1,2]->9, [3,1,2]->9, [5,1,2]->9, etc.
    """
    def to_key(self, ctx):
        return tuple(ctx.neighbourhood_activities)


class _UnorderedMemoizationKey(MemoizationKey):
    """
    An implementation of a memoization key that simply converts the context's neighbourhood activities into
    a frozenset of item counts. This assumes that the ordering of the nodes in the neighbourhood doesn't matter.
    For example, a totalistic 1D CA rule does not require an ordering of the neighbourhood to be specified.
    It would be less efficient to just return a tuple of the activities here, since we'd end up with needless
    entries in the cache. The rule doesn't depend on node order, so states like (1,0,1) and (0,1,1) should result
    in the same cache hit, and evaluate to the same result.

    Note that this implementation doesn't include the current node if it isn't in its neighbourhood. If the rule
    depends on the current node, but the current node isn't in its neighbourhood, then the user should supply their
    own memoization key that adds the current node's activity. If the rule doesn't depend on the current node's
    activity, then we'd be adding cache entries unnecessarily if we added the current node to the key.
    e.g. [1,0,2], [2,3,1], [2,5,1], etc. all map to 9, so all we really need is a cache entry with {1,2}->9, but
    instead we'd end up adding the entries (0,{1,2})->9, (3,{1,2})->9, (5,{1,2})->9, etc.
    """
    def to_key(self, ctx):
        return frozenset(collections.Counter(ctx.neighbourhood_activities).items())


def evolve_topology(topology_rule, t, activities, prev_network, trajectory, copy_network,
                    persist_network, added_nodes=None, removed_nodes=None):
    network = prev_network
    if added_nodes or removed_nodes:
        network = network.copy()

        # adjust connectivity map according to node deletions and insertions
        for node_label in removed_nodes:
            network.remove_node(node_label)

        for activity, outgoing_links, node_label in added_nodes:
            network.add_node(node_label, activity=check_np(activity))
            for target, connection_state in outgoing_links.items():
                network.add_edge(node_label, target, **connection_state)

    if topology_rule:
        if copy_network:
            network = network.copy()
        network = topology_rule(TopologyContext(network, activities, t))
        if not network:
            raise Exception("topology rule must return a network")

    if persist_network:
        trajectory[t].network = network

    return network


def _get_past_activities(past_conditions, trajectory, t):
    if past_conditions and len(past_conditions) > 0:
        past_activities = [None]*len(past_conditions)
        last_t = t - 1
        for i in range(len(past_conditions)-1, -1, -1):

            curr_past_cond = past_conditions[last_t-1] if last_t < 1 else trajectory[last_t-1].activities
            if not isinstance(curr_past_cond, dict) and isinstance(curr_past_cond, (list, np.ndarray)):
                curr_past_cond = {i: v for i, v in enumerate(curr_past_cond)}

            past_activities[i] = curr_past_cond
            last_t -= 1
        return past_activities
    return None


def _get_neighbourhood_map(network):
    if network.rotation_system is not None:
        return network.rotation_system
    return {node_label: [i for i in network.in_edges(node_label)] for node_label in network.nodes}


def _get_input_function(timesteps=None, input=None):
    if timesteps is None and input is None:
        raise Exception("either the timesteps or input must be provided")

    if input is not None:
        if callable(input):
            return input
        else:
            return _ListInputFunction(input)

    return _TimestepInputFunction(timesteps)


def _is_indexable(obj):
    return isinstance(obj, collections.Sequence)


class _TimestepInputFunction:
    def __init__(self, num_steps):
        self._num_steps = num_steps

    def __call__(self, t, activities, network):
        if t == self._num_steps:
            return None
        return "__timestep__"


class _ListInputFunction:
    def __init__(self, input_list):
        self._input_list = input_list

    def __call__(self, t, activities, network):
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


def check_np(obj):
    if isinstance(obj, np.generic):
        return np.asscalar(obj)
    return obj
