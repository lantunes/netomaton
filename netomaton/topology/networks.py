from . import adjacency
import networkx as nx
import numpy as np
import netomaton as ntm
from collections import deque


def _shift_to_center(nodes, node_to_center_on):
    """
    Shifts the given node list such that the specified node is at the center.
    NOTE: this is meant to be used by 1D CA systems, where a node label is simply the index of the node

    :param nodes: a list of nodes (in terms of their labels)

    :param node_to_center_on: the node to center on

    :return: a nodes that has been rotated so that the specified node is at the center
    """
    center = len(nodes) // 2
    shifted = deque(sorted(nodes))

    def index_of(arr, val):
        return np.where(arr == val)[0][0] if type(arr) == np.ndarray else arr.index(val)
    shifted.rotate(center - index_of(nodes, node_to_center_on))
    return list(shifted)


def cellular_automaton(n=200, r=1, ordered=True, periodic=True):
    adjacency_matrix = adjacency.cellular_automaton(n, r, boundary="periodic")
    network = from_adjacency_matrix(adjacency_matrix)
    if ordered:
        network.rotation_system = {node: _shift_to_center(list(network.in_edges(node).keys()), node)
                                   for node in network.nodes}
    return network


def cellular_automaton2d(rows, cols, r=1, neighbourhood="Moore", ordered=True, periodic=True):
    adjacency_matrix = adjacency.cellular_automaton2d(rows, cols, r, neighbourhood, "periodic")
    network = from_adjacency_matrix(adjacency_matrix)
    if ordered:
        network.rotation_system = {node: _shift_to_center(list(network.in_edges(node).keys()), node)
                                   for node in network.nodes}
    return network


def lattice(dim, periodic=False, self_loops=False, first_label=0):
    """
    Returns a bi-directional n-dimensional lattice (i.e. Euclidean) network.

    :param dim: a triple, representing the number of dimensions of the lattice

    :param periodic: whether the lattice is periodic (default is False)

    :param self_loops: if True, each node has a connection to itself (default is False)

    :param first_label: an integer specifying the first node label (default is 1)

    :return: a network
    """
    G = nx.grid_graph(dim=dim, periodic=periodic)
    G = nx.convert_node_labels_to_integers(G, first_label=first_label)
    network = ntm.Network()
    for edge in G.edges:
        if edge[0] == edge[1] and not self_loops:
            continue
        network.add_edge(edge[1], edge[0])
        network.add_edge(edge[0], edge[1])
    return network


def disconnected(nodes):
    """
    Create a fully disconnected network.

    :param nodes: either an int, containing the number of nodes, or a list, containing the node labels to use

    :return: a fully disconnected network
    """
    network = ntm.Network(n=nodes) if isinstance(nodes, int) else ntm.Network()
    if isinstance(nodes, (list, np.ndarray)):
        [network.add_node(n) for n in nodes]
    return network


def from_adjacency_matrix(adj):
    network = ntm.Network()
    for i, row in enumerate(adj):
        for j, val in enumerate(row):
            if val != 0:
                network.add_edge(i, j, weight=val)
    return network


def watts_strogatz_graph(n, k, p, seed=None):
    """
    Returns a Watts-Strogatz small-world graph as a Network.

    :param n: the number of nodes

    :param k: the number of nearest neighbours a node joins to

    :param p: the probability of re-connecting each edge

    :param seed: integer, random_state, or None (default); a random seed to use for random number generation

    :return: a Network
    """
    G = nx.watts_strogatz_graph(n, k, p, seed)
    adjacency = nx.adjacency_matrix(G).todense().tolist()
    return from_adjacency_matrix(adjacency)


def bipartite(set1, set2, edge_attributes=None):
    """
    Returns a bipartite graph as a Network, with bidirectional edges.

    To supply attributes for the edges, use the `edge_attributes` parameter. For example:
    ```
    edge_attributes = {
        0: {3: {"weight": 0.1}, 4: {"weight": 0.2}},
        1: {3: {"weight": 0.3}, 4: {"weight": 0.4}},
        2: {3: {"weight": 0.5}, 4: {"weight": 0.6}}
    }
    ```
    The example above implies that `set1` contains {0, 1, 2} and `set2` contains {3, 4}. The "weight"
    attribute is set on each edge accordingly.

    :param set1: the node labels of the first set

    :param set2: the node labels of the second set

    :param edge_attributes: a dict where each key is a node label from set1, and each value is a dict where each key
                            is a node label from set2 and each value is a dict with the attributes

    :return: a Network
    """
    network = ntm.Network()
    for node1 in set1:
        for node2 in set2:
            if edge_attributes is None:
                network.add_edge_bidir(node1, node2)
            else:
                attrs = edge_attributes[node1][node2]
                network.add_edge_bidir(node1, node2, **attrs)
    return network


def complete(n):
    """
    Returns a fully connected Network (i.e. a complete graph) with `n` nodes.

    :param n: the number of nodes in the Network

    :return: a fully-connected Network
    """
    G = nx.complete_graph(n)
    adjacency = nx.adjacency_matrix(G).todense().tolist()
    return from_adjacency_matrix(adjacency)
