import networkx as nx
import numpy as np
import netomaton as ntm


def lattice(dim, periodic=False, self_loops=False, first_label=1):
    """
    Returns a bi-directional n-dimensional lattice (i.e. Euclidean) network.
    :param dim: a triple, representing the number of dimensions of the lattice
    :param periodic: whether the lattice is periodic (default is False)
    :param self_loops: if True, each node has a connection to itself (default is False)
    :param first_label: an integer specifying the first node label (default is 1)
    :return: a connectivity map
    """
    G = nx.grid_graph(dim=dim, periodic=periodic)
    G = nx.convert_node_labels_to_integers(G, first_label=first_label)
    connectivity_map = {}
    for edge in G.edges:
        if edge[0] == edge[1] and not self_loops:
            continue
        if edge[0] not in connectivity_map:
            connectivity_map[edge[0]] = {}
        connectivity_map[edge[0]].update({edge[1]: [{}]})
        if edge[1] not in connectivity_map:
            connectivity_map[edge[1]] = {}
        connectivity_map[edge[1]].update({edge[0]: [{}]})
    return connectivity_map


def disconnected(nodes):
    """
    Create a fully disconnected network in the form of a connectivity map.
    :param nodes: either an int, containing the number of nodes, or a list, containing the node labels to use
    :return: a fully disconnected network connectivity map
    """
    if isinstance(nodes, (list, np.ndarray)):
        return {n: {} for n in nodes}
    return {n: {} for n in range(nodes)}
