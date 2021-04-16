import numpy as np
import networkx as nx
from enum import Enum
from .utils import copy_network


class NodeContext_NX(object):
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
    def add_node(self, activity, outgoing_links, nodel_label):
        self.added_nodes.append((activity, outgoing_links, nodel_label))

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


class TopologyContext(object):

    __slots__ = ("network", "activities", "timestep")

    def __init__(self, network, activities, t):
        self.network = network
        self.activities = activities
        self.timestep = t
        

class UpdateOrder_NX(Enum):
    ACTIVITIES_FIRST = 1
    TOPOLOGY_FIRST = 2
    SYNCHRONOUS = 3


def evolve_nx(network, timesteps, initial_conditions=None, activity_rule=None, topology_rule=None, 
              update_order=UpdateOrder_NX.ACTIVITIES_FIRST):
    if initial_conditions is None:
        initial_conditions = {}

    # convert initial_conditions to map, if it isn't already
    if not isinstance(initial_conditions, dict) and isinstance(initial_conditions, (list, np.ndarray)):
        initial_conditions = {i: {"activity": v} for i, v in enumerate(initial_conditions)}

    # TODO should we keep the activities inside the network?
    #  there are some advantages to keeping them separate, and some disadvantages
    nx.set_node_attributes(network, initial_conditions)

    network_over_time = {0: network}

    for t in range(1, timesteps):

        prev_activities = nx.get_node_attributes(network_over_time[t - 1], "activity")
        network_over_time[t] = copy_network(network_over_time[t - 1])

        if update_order is UpdateOrder_NX.ACTIVITIES_FIRST:
            added_nodes, removed_nodes = _evolve_activities(t, activity_rule, prev_activities,
                                                            network_over_time[t], network_over_time)
            new_activities = nx.get_node_attributes(network_over_time[t], "activity")
            _evolve_topolgy(t, topology_rule, network_over_time[t], new_activities, network_over_time,
                            added_nodes, removed_nodes)

        elif update_order is UpdateOrder_NX.TOPOLOGY_FIRST:
            _evolve_topolgy(t, topology_rule, network_over_time[t], prev_activities, network_over_time)
            # added and removed nodes are ignore in this case
            _evolve_activities(t, activity_rule, prev_activities, network_over_time[t], network_over_time)

        elif update_order is UpdateOrder_NX.SYNCHRONOUS:
            _evolve_topolgy(t, topology_rule, network_over_time[t], prev_activities, network_over_time)
            # added and removed nodes are ignore in this case
            _evolve_activities(t, activity_rule, prev_activities, network_over_time[t - 1], network_over_time)

        else:
            raise Exception("unsupported update_order: %s" % update_order)

    # TODO we should return a list of networks instead of a dict
    return network_over_time


def _evolve_activities(t, activity_rule, prev_activities, network, network_over_time):
    added_nodes = []
    removed_nodes = []
    
    if activity_rule:
        for node_label in network.nodes:
            in_edges = network.in_edges(node_label, data=True)
            neighbour_labels = [i[0] for i in in_edges]
            incoming_connections = _get_incoming_connections(in_edges)
            current_activity = prev_activities[node_label]
            neighbourhood_activities = [prev_activities[neighbour_label] for neighbour_label in neighbour_labels]
            # node_in = None if inp == "__timestep__" else inp[node_label] if _is_indexable(inp) else inp
            ctx = NodeContext_NX(node_label, t, prev_activities, neighbour_labels, neighbourhood_activities,
                                 incoming_connections, current_activity, None, None)
            new_activity = activity_rule(ctx)

            if ctx.added_nodes:
                added_nodes.extend(ctx.added_nodes)
            if ctx.removed_nodes:
                removed_nodes.extend(ctx.removed_nodes)

            if node_label not in ctx.removed_nodes:
                network_over_time[t].nodes[node_label]["activity"] = new_activity

    return added_nodes, removed_nodes


def _evolve_topolgy(t, topology_rule, network, activities, network_over_time, added_nodes=None, removed_nodes=None):
    if added_nodes or removed_nodes:
        # adjust connectivity map according to node deletions and insertions
        for node_label in removed_nodes:
            network.remove_node(node_label)

        for activity, outgoing_links, node_label in added_nodes:
            network.add_node(node_label, activity=activity)
            for target, connection_state in outgoing_links.items():
                network.add_edge(node_label, target, **connection_state)
    
    if topology_rule:
        network = topology_rule(TopologyContext(network, activities, t))
        if not network:
            raise Exception("topology rule must return a network")
        
    network_over_time[t] = network


def _get_incoming_connections(in_edges):
    incoming = {}
    for i in in_edges:
        if i[0] not in incoming:
            incoming[i[0]] = []
        incoming[i[0]].append(i[2])
    return incoming
