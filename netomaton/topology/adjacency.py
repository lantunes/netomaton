import networkx as nx
import numpy as np

# TODO provide a connectivity_map.py, that does everything here, except returns connectivity maps


def cellular_automaton(n, r=1, boundary="periodic"):
    """
    Creates the adjacency matrix for a 1D cellular automaton, with the given number of cells and neighbourhood
    radius.
    :param n: the number of cells in this automaton
    :param r: the neighbourhood radius
    :param boundary: the boundary condition
    :return: an adjacency matrix describing this cellular automaton
    """
    if n < 3:
        raise Exception("There must be at least 3 cells")
    adjacency_matrix = [[0. for j in range(n)] for i in range(n)]
    if boundary == "periodic":
        for w, row in enumerate(adjacency_matrix):
            for c, _ in enumerate(row):
                if w == c:
                    adjacency_matrix[w][c] = 1.
                    for i in range(r):
                        adjacency_matrix[w][c - (1 + i)] = 1.
                        adjacency_matrix[w][(c + (1 + i)) % len(adjacency_matrix[w])] = 1.
    else:
        raise Exception("unsupported boundary condition: %s" % boundary)
    return adjacency_matrix


def cellular_automaton2d(rows, cols, r=1, neighbourhood='Moore', boundary="periodic"):
    """
    Creates the adjacency matrix for a 2D cellular automaton, with the given number of rows, columns, neighbourhood
    radius, and neighbourhood type.
    :param rows: the number of rows in the 2D automaton
    :param cols: the number of columns in the 2D automaton
    :param r: the neighbourhood radius; the neighbourhood dimensions will be 2r+1 x 2r+1
    :param neighbourhood: the neighbourhood type; valid values are 'Moore', 'von Neumann', and 'Hex'
    :param boundary: the boundary condition
    :return: an adjacency matrix describing this cellular automaton
    """
    n = rows * cols
    if n < 9:
        raise Exception("There must be at least 9 cells")
    adjacency_matrix = [[0. for j in range(n)] for i in range(n)]
    if boundary == "periodic":
        if neighbourhood == 'von Neumann':
            criteria = lambda a_i, b_i, a_o, b_o, radius, rownum: np.abs(a_i - a_o) + np.abs(b_i - b_o) <= radius
        elif neighbourhood == 'Moore':
            criteria = lambda a_i, b_i, a_o, b_o, radius, rownum: np.abs(a_i - a_o) <= radius and np.abs(b_i - b_o) <= radius
        elif neighbourhood == 'Hex':
            def hex_crit(a_i, b_i, a_o, b_o, radius, rownum):
                vn = np.abs(a_i - a_o) + np.abs(b_i - b_o) <= radius
                if rownum % 2 == 0:
                    ex = (b_i - b_o) < radius
                else:
                    ex = (b_o - b_i) < radius
                return vn or ex
            criteria = hex_crit
        else:
            raise Exception("neighbourhood type not supported: %s" % neighbourhood)

        lattice = np.array(range(n)).reshape((rows, cols)).tolist()
        rownum = 0
        for a, row in enumerate(lattice):
            rownum += 1
            for b, _ in enumerate(row):
                adjacency_row_num = lattice[a][b]
                neighbourhood_points = _get_neighbourhood_points2d(a, b, r, criteria, rownum)
                for point in neighbourhood_points:
                    x = point[0] if point[0] == -1 else point[0] % len(lattice)
                    y = point[1] if point[1] == -1 else point[1] % len(lattice[a])
                    adjacency_matrix[adjacency_row_num][lattice[x][y]] = 1.

    else:
        raise Exception("unsupported boundary condition: %s" % boundary)
    return adjacency_matrix


def _get_neighbourhood_points2d(a, b, r, criteria, rownum):
    neighbourhood_points = [[(x, y) for y in range(b-r, b+r+1)] for x in range(a-r, a+r+1)]
    filtered = [[p for p in row if criteria(p[0], p[1], a, b, r, rownum)] for row in neighbourhood_points]
    return [item for sublist in filtered for item in sublist]  # flatten the list of lists


def watts_strogatz_graph(n, k, p, as_list=True, seed=None):
    """
    Returns a Watts-Strogatz small-world graph as an adjacency matrix.
    If `as_list` is `True`, then a Python list of lists is returned, otherwise a NumPy matrix object is
    returned. A Python list of lists is addressable with `A[i][j]`, whereas a NumPy matrix is addressable
    with `A[i, j]`. For large matrices, it is faster to return a NumPy matrix (i.e. `as_list=False`).
    :param n: the number of nodes
    :param k: the number of nearest neighbours a node joins to
    :param p: the probability of re-connecting each edge
    :param as_list: if True (default), returns a Python list of lists, otherwise returns a NumPy matrix
    :param seed: integer, random_state, or None (default); a random seed to use for random number generation
    :return: the adjacency matrix
    """
    G = nx.watts_strogatz_graph(n, k, p, seed)
    a = nx.adjacency_matrix(G).todense()
    if as_list:
        a = a.tolist()
    return a


def lattice(dim, periodic=False, as_list=True, self_loops=False, first_label=0):
    """
    Returns a bi-directional n-dimensional lattice (i.e. Euclidean) network as an adjacency matrix.
    If `as_list` is `True`, then a Python list of lists is returned, otherwise a NumPy matrix object is
    returned. A Python list of lists is addressable with `A[i][j]`, whereas a NumPy matrix is addressable
    with `A[i, j]`. For large matrices, it is faster to return a NumPy matrix (i.e. `as_list=False`).
    :param dim: a triple, representing the number of dimensions of the lattice
    :param periodic: whether the lattice is periodic (default is False)
    :param as_list: if True (default), returns a Python list of lists, otherwise returns a NumPy matrix
    :param self_loops: if True, each node has a connection to itself (default is False)
    :param first_label: an integer specifying the first node label (default is 0)
    :return: the adjacency matrix
    """
    G = nx.grid_graph(dim=dim, periodic=periodic)
    G = nx.convert_node_labels_to_integers(G, first_label=first_label)
    G = G.to_directed()
    a = nx.adjacency_matrix(G).todense()
    if not self_loops:
        np.fill_diagonal(a, 0)
    if as_list:
        a = a.tolist()
    return a
