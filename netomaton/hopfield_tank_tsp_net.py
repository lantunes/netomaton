import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class HopfieldTankTSPNet:
    """
    Based on J. J. Hopfield and D. W. Tank, Biol. Cybern: 52, 141-152 (1985).
    """
    def __init__(self, points, dt=1.00, A=500, B=500, C=200, D=500, u_0=0.02, n=15):
        """
        A point is a tuple (x, y), where x is the x-coordinate and y is the y-coordinate of the point.
        :param points: a list of tuples, where each tuple represents a point's x and y coordinates
        :param dt: the size of the timestep
        :param A: a hyparameter
        :param B: a hyparameter
        :param C: a hyparameter
        :param D: a hyparameter
        :param u_0: a hyparameter
        :param n: a hyparameter
        """
        self._points = points
        self._dt = dt
        self._A = A
        self._B = B
        self._C = C
        self._D = D
        self._u_0 = u_0
        self._n = n
        self._distances_map = self._get_distances_map(self.get_distances())
        self._cell_label_map = self._get_cell_label_map(points)
        self._coordinate_map = self._get_coordinate_map(self._cell_label_map)
        self._adjacencies = self._get_adjacencies(self._cell_label_map)

    def get_distances(self):
        """
        A point is a tuple (x, y), where x is the x-coordinate and y is the y-coordinate of the point.
        :param points: a list of tuples, where each tuple represents a point's x and y coordinates
        :return: a list of n-choose-2 triples (A, B, d), where A is the index of point A, B is the index of point B,
                 and d is the distance between them
        """
        distances = []
        i = 0
        while i < len(self._points) - 1:
            from_point = self._points[i]
            for j in range(i + 1, len(self._points)):
                to_point = self._points[j]
                d = math.sqrt((to_point[0] - from_point[0]) ** 2 + (to_point[1] - from_point[1]) ** 2)
                distances.append((i, j, d))
            i += 1

        return distances

    def get_permutation_matrix(self, activities):
        return activities[-1].reshape(len(self._points), len(self._points))

    def get_tour_graph(self, points, permutation_matrix):
        """
        A point is a tuple (x, y), where x is the x-coordinate and y is the y-coordinate of the point.
        The permutation_matrix is n x n matrix, where n is the number of points in the TSP. Each row represents a point,
        and each column represents the position of that point in the tour.
        :param points: the list of points (tuples) which represent the points in the TSP
        :param permutation_matrix: an n x n matrix, where n is the number of points, which represents the final tour
        :return: a NetworkX Graph representing the tour, a dictionary defining the NetworkX positions for the Graph, and
                 the total tour length
        """
        assert len(points) == len(permutation_matrix), \
            "the number of rows in permutation_matrix does not match the number of points"
        assert len(points) == len(permutation_matrix[0]), \
            "the number of columns in permutation_matrix does not match the number of points"

        G = nx.Graph()
        for point_index in range(len(points)):
            G.add_node(point_index)

        tour_index_to_point_index = {}

        for point_index, row in enumerate(permutation_matrix):
            tour_index = np.argmax(row)
            if tour_index in tour_index_to_point_index:
                raise Exception("a point has already claimed position #%s in the tour" % str(tour_index + 1))
            tour_index_to_point_index[tour_index] = point_index

        # #
        # import scipy.stats as ss
        # permutation_matrix = permutation_matrix.transpose()[0]
        # print(permutation_matrix)
        # print(ss.rankdata(permutation_matrix))
        # ranked = []
        # for s in ss.rankdata(permutation_matrix):
        #     ranked.append(np.abs(s - 10.))
        # print(ranked)
        # for i, r in enumerate(ranked):
        #     tour_index_to_point_index[r] = i
        # #

        distances = []

        for tour_index, point_index in tour_index_to_point_index.items():
            from_point_index = point_index
            to_point_index = tour_index_to_point_index[(tour_index + 1) % len(points)]
            G.add_edge(from_point_index, to_point_index)

            from_point = points[from_point_index]
            to_point = points[to_point_index]
            distances.append(math.sqrt((to_point[0] - from_point[0]) ** 2 + (to_point[1] - from_point[1]) ** 2))

        pos = {i: point for i, point in enumerate(points)}

        return G, pos, sum(distances)

    def plot_tour(self, G, pos):
        """
        Renders the points and tour.
        :param G: a NetworkX Graph representing the points and the tour
        :param pos: a dictionary defining the NetworkX positions for the Graph
        """
        nx.draw_networkx(G, pos)
        plt.show()

    def _get_distances_map(self, distances):
        """
        Given a list of n-choose-2 triples (A, B, d), where A is the index of point A, B is the index of point B,
        and d is the distance between them, returns a dictionary where the keys are a tuple, (A, B), and the values are the
        distances between A and B.
        :param distances: a list of n-choose-2 triples (A, B, d), where A is the index of point A, B is the index of point B,
                          and d is the distance between them
        :return: a dictionary where the keys are a tuple, (A, B), and the values are the
                 distances between A and B
        """
        distances_map = {}
        for a, b, d in distances:
            distances_map[(a, b)] = d
            distances_map[(b, a)] = d
            distances_map[(a, a)] = 0.0
            distances_map[(b, b)] = 0.0
        return distances_map

    def _get_cell_label_map(self, points):
        """
        Returns a dictionary where the keys are the cell indices (there are n^2 cells, where n is the number of points),
        and the values are a tuple (row, col), representing the row index and column index of the cell in the permutation
        matrix (the matrix describing the tour, where each row represents a point, and each column represents the position
        of that point in the tour.
        :param points: a list of tuples, where each tuple represents a point's x and y coordinates
        :return: a dictionary with cell indices as keys and tuple (row, col) for the position of the cell in the permutation
                 matrix as values
        """
        cell_label_map = {}
        num_points = len(points)
        current_point = 0
        current_cell = 0
        while current_point < num_points:
            for n in range(num_points):
                cell_label_map[current_cell] = (current_point, n)
                current_cell += 1
            current_point += 1
        return cell_label_map

    def _get_coordinate_map(self, cell_label_map):
        coordinate_map = {}
        for cell_index, coords in cell_label_map.items():
            coordinate_map[coords] = cell_index
        return coordinate_map

    def _get_adjacencies(self, cell_label_map):
        # adjacencies = []
        # num_cells = len(cell_label_map)
        # num_points = int(math.sqrt(num_cells))
        # for c in range(num_cells):
        #     row, col = cell_label_map[c]
        #     conn = [0 for _ in range(num_cells)]
        #     for c2 in range(num_cells):
        #         row2, col2 = cell_label_map[c2]
        #         if row2 == row or col2 == col or col2 == ((col - 1) % num_points) or col2 == ((col + 1) % num_points):
        #             conn[c2] = 1
        #     adjacencies.append(conn)
        # return adjacencies

        # fully connected network
        return [[1 for _ in range(len(cell_label_map))] for _ in range(len(cell_label_map))]

    @property
    def adjacencies(self):
        return self._adjacencies

    def _V(self, u):
        return (1/2) * (1 + math.tanh(u / self._u_0))

    def _get_opposite_neighbour_activity(self, activities, neighbour_indices, opposite_neighbour_index):
        for i, n in enumerate(neighbour_indices):
            if n == opposite_neighbour_index:
                return activities[i]
        raise Exception("could not find the opposite neighbour index: %d" % opposite_neighbour_index)

    def activity_rule(self, n, c, t):
        current_activity = n.current_activity
        cell_row, cell_col = self._cell_label_map[c]

        A_sum = 0
        B_sum = 0
        C_sum = 0
        D_sum = 0
        for i, neighbour_activity in enumerate(n.activities):
            neighbour_index = n.neighbour_indices[i]
            neighbour_cell_row, neighbour_cell_col = self._cell_label_map[neighbour_index]

            if neighbour_cell_row == cell_row and neighbour_cell_col != cell_col:
                A_sum += self._V(neighbour_activity)

            if neighbour_cell_col == cell_col and neighbour_cell_row != cell_row:
                B_sum += self._V(neighbour_activity)

            # global inhibition
            C_sum += (self._V(neighbour_activity) - self._n)

            if neighbour_cell_col == ((cell_col - 1) % len(self._points)):
                opp_neighbour_index = self._coordinate_map[(neighbour_cell_row, (cell_col + 1) % len(self._points))]
                opp_neighbour_activity = self._get_opposite_neighbour_activity(n.activities, n.neighbour_indices, opp_neighbour_index)
                D_sum += (self._distances_map[(neighbour_cell_row, cell_row)] * (self._V(neighbour_activity) + self._V(opp_neighbour_activity)))

        activity = (-current_activity) - (self._A * A_sum) - (self._B * B_sum) - (self._C * C_sum) - (self._D * D_sum)

        return current_activity + (self._dt * activity)

