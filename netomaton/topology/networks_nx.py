from . import adjacency
import networkx as nx
import numpy as np


def cellular_automaton(n=200, r=1, periodic=True):
    adjacency_matrix = adjacency.cellular_automaton(n, r, boundary="periodic")
    return nx.from_numpy_array(np.array(adjacency_matrix), create_using=nx.DiGraph)


def cellular_automaton2d(rows, cols, r=1, neighbourhood='Moore', periodic=True):
    adjacency_matrix = adjacency.cellular_automaton2d(rows, cols, r, neighbourhood, "periodic")
    return nx.from_numpy_array(np.array(adjacency_matrix), create_using=nx.DiGraph)


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
    connectivity_map = nx.DiGraph()
    for from_node, to_node in G.edges:
        if from_node == to_node and not self_loops:
            continue
        connectivity_map.add_edge(to_node, from_node)
        connectivity_map.add_edge(from_node, to_node)
    return connectivity_map


def disconnected(nodes, to_create=nx.DiGraph):
    """
    Create a fully disconnected network in the form of a connectivity map.
    :param nodes: either an int, containing the number of nodes, or a list, containing the node labels to use
    :return: a fully disconnected network connectivity map
    """
    G = to_create()
    if isinstance(nodes, (list, np.ndarray)):
        [G.add_node(n) for n in nodes]
    else:
        [G.add_node(n) for n in range(nodes)]
    return G
