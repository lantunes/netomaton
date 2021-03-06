from . import adjacency
import networkx as nx
import numpy as np
import netomaton as ntm


def cellular_automaton(n=200, r=1, periodic=True):
    adjacency_matrix = adjacency.cellular_automaton(n, r, boundary="periodic")
    return from_adjacency_matrix(adjacency_matrix)


def cellular_automaton2d(rows, cols, r=1, neighbourhood='Moore', periodic=True):
    adjacency_matrix = adjacency.cellular_automaton2d(rows, cols, r, neighbourhood, "periodic")
    return from_adjacency_matrix(adjacency_matrix)


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

    :return: as Network
    """
    G = nx.watts_strogatz_graph(n, k, p, seed)
    adjacency = nx.adjacency_matrix(G).todense().tolist()
    return from_adjacency_matrix(adjacency)
