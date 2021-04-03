import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class HopfieldTankTSPNet:
    """
    Based on J. J. Hopfield and D. W. Tank, "'Neural' Computation of Decisions in Optimization Problems",
    Biol. Cybern: 52, 141-152 (1985).
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
        self._node_label_map = self._get_node_label_map(points)
        self._coordinate_map = self._get_coordinate_map(self._node_label_map)
        self._adjacency_matrix = self._get_adjacency_matrix(self._node_label_map)

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
        if not isinstance(activities, np.ndarray):
            activities = np.array(activities)
        f = lambda u: self._V(u)
        return f(activities[-1].reshape(len(self._points), len(self._points)))

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

    def _get_node_label_map(self, points):
        """
        Returns a dictionary where the keys are the node indices (there are n^2 nodes, where n is the number of points),
        and the values are a tuple (row, col), representing the row index and column index of the node in the permutation
        matrix (the matrix describing the tour, where each row represents a point, and each column represents the position
        of that point in the tour.
        :param points: a list of tuples, where each tuple represents a point's x and y coordinates
        :return: a dictionary with node indices as keys and tuple (row, col) for the position of the node in the permutation
                 matrix as values
        """
        node_label_map = {}
        num_points = len(points)
        current_point = 0
        current_node = 0
        while current_point < num_points:
            for n in range(num_points):
                node_label_map[current_node] = (current_point, n)
                current_node += 1
            current_point += 1
        return node_label_map

    def _get_coordinate_map(self, node_label_map):
        coordinate_map = {}
        for node_index, coords in node_label_map.items():
            coordinate_map[coords] = node_index
        return coordinate_map

    def _get_adjacency_matrix(self, node_label_map):
        # fully connected network
        return [[1 for _ in range(len(node_label_map))] for _ in range(len(node_label_map))]

    @property
    def adjacency_matrix(self):
        return self._adjacency_matrix

    def _V(self, u):
        return (1/2) * (1 + np.tanh(u / self._u_0))

    def _get_opposite_neighbour_activity(self, activities, neighbour_indices, opposite_neighbour_label):
        for i, n in enumerate(neighbour_indices):
            if n == opposite_neighbour_label:
                return activities[i]
        raise Exception("could not find the opposite neighbour index: %d" % opposite_neighbour_label)

    def activity_rule(self, ctx):
        current_activity = ctx.current_activity
        node_row, node_col = self._node_label_map[ctx.node_label]

        A_sum = 0
        B_sum = 0
        C_sum = 0
        D_sum = 0
        for i, neighbour_activity in enumerate(ctx.neighbourhood_activities):
            neighbour_label = ctx.neighbour_labels[i]
            neighbour_node_row, neighbour_node_col = self._node_label_map[neighbour_label]

            if neighbour_node_row == node_row and neighbour_node_col != node_col:
                A_sum += self._V(neighbour_activity)

            if neighbour_node_col == node_col and neighbour_node_row != node_row:
                B_sum += self._V(neighbour_activity)

            # global inhibition
            C_sum += self._V(neighbour_activity)

            if neighbour_node_col == ((node_col - 1) % len(self._points)):
                opp_neighbour_label = self._coordinate_map[(neighbour_node_row, (node_col + 1) % len(self._points))]
                opp_neighbour_activity = self._get_opposite_neighbour_activity(ctx.neighbourhood_activities, ctx.neighbour_labels, opp_neighbour_label)
                D_sum += (self._distances_map[(neighbour_node_row, node_row)] * (self._V(neighbour_activity) + self._V(opp_neighbour_activity)))

        activity = (-current_activity) - (self._A * A_sum) - (self._B * B_sum) - (self._C * (C_sum - self._n)) - (self._D * D_sum)

        return current_activity + (self._dt * activity)

