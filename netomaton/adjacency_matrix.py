from math import sqrt

import networkx as nx
import numpy as np


class AdjacencyMatrix:
    @staticmethod
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

    @staticmethod
    def cellular_automaton2d(n, r=1, neighbourhood='Moore', boundary="periodic"):
        """
        Creates the adjacency matrix for a 2D cellular automaton, with the given number of cells, neighbourhood
        radius, and neighbourhood type.
        :param n: the number of cells in this automaton
        :param r: the neighbourhood radius; the neighbourhood dimensions will be 2r+1 x 2r+1
        :param neighbourhood: the neighbourhood type; valid values are 'Moore' or 'von Neumann'
        :param boundary: the boundary condition
        :return: an adjacency matrix describing this cellular automaton
        """
        if n < 9:
            raise Exception("There must be at least 9 cells")
        if n % sqrt(n) != 0.0:
            raise Exception("The number of cells must be a perfect square")
        adjacency_matrix = [[0. for j in range(n)] for i in range(n)]
        if boundary == "periodic":
            if neighbourhood == 'von Neumann':
                criteria = lambda a_i, b_i, a_o, b_o, radius: np.abs(a_i - a_o) + np.abs(b_i - b_o) <= radius
            elif neighbourhood == 'Moore':
                criteria = lambda a_i, b_i, a_o, b_o, radius: np.abs(a_i - a_o) <= radius and np.abs(b_i - b_o) <= radius
            else:
                raise Exception("neighbourhood type not supported: %s" % neighbourhood)

            lattice = np.array(range(n)).reshape((int(sqrt(n)), int(sqrt(n)))).tolist()
            for a, row in enumerate(lattice):
                for b, _ in enumerate(row):
                    adjacency_row_num = lattice[a][b]
                    neighbourhood_points = AdjacencyMatrix._get_neighbourhood_points2d(a, b, r, criteria)
                    for point in neighbourhood_points:
                        x = point[0] if point[0] == -1 else point[0] % len(lattice[a])
                        y = point[1] if point[1] == -1 else point[1] % len(lattice[a])
                        adjacency_matrix[adjacency_row_num][lattice[x][y]] = 1.

        else:
            raise Exception("unsupported boundary condition: %s" % boundary)
        return adjacency_matrix

    @staticmethod
    def _get_neighbourhood_points2d(a, b, r, criteria):
        neighbourhood_points = [[(x, y) for y in range(b-r, b+r+1)] for x in range(a-r, a+r+1)]
        filtered = [[p for p in row if criteria(p[0], p[1], a, b, r)] for row in neighbourhood_points]
        return [item for sublist in filtered for item in sublist]  # flatten the list of lists

    @staticmethod
    def watts_strogatz_graph(n, k, p):
        G = nx.watts_strogatz_graph(n, k, p)
        return nx.adjacency_matrix(G).todense().tolist()