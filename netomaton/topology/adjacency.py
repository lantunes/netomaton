import numpy as np


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
