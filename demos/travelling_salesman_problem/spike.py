import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_distances(points):
    """
    A point is a tuple (x, y), where x is the x-coordinate and y is the y-coordinate of the point.
    :param points: a list of tuples, where each tuple represents a point's x and y coordinates
    :return: a list of n-choose-2 triples (A, B, d), where A is the index of point A, B is the index of point B,
             and d is the distance between them
    """
    distances = []
    i = 0
    while i < len(points) - 1:
        from_point = points[i]
        for j in range(i+1, len(points)):
            to_point = points[j]
            d = math.sqrt((to_point[0] - from_point[0])**2 + (to_point[1] - from_point[1])**2)
            distances.append((i, j, d))
        i += 1

    return distances


def get_distances_map(distances):
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


def get_tour_graph(points, activities):
    """
    A point is a tuple (x, y), where x is the x-coordinate and y is the y-coordinate of the point.
    The activities are n x n matrix, where n is the number of points in the TSP. Each row represents a point, and each
    column represents the position of that point in the tour.
    :param points: the list of points (tuples) which represent the points in the TSP
    :param activities: an n x n matrix, where n is the number of points, which represents the final tour
    :return: a NetworkX Graph representing the tour, a dictionary defining the NetworkX positions for the Graph, and
             the total tour length
    """
    assert len(points) == len(activities), "the number of rows in activities does not match the number of points"
    assert len(points) == len(activities[0]), "the number of columns in activities does not match the number of points"

    G = nx.Graph()
    for point_index in range(len(points)):
        G.add_node(point_index)

    tour_index_to_point_index = {}
    for point_index, row in enumerate(activities):
        tour_index = np.argmax(row)
        if tour_index in tour_index_to_point_index:
            raise Exception("a point has already claimed position #%s in the tour" % str(tour_index+1))
        tour_index_to_point_index[tour_index] = point_index

    distances = []

    for tour_index, point_index in tour_index_to_point_index.items():
        from_point_index = point_index
        to_point_index = tour_index_to_point_index[(tour_index + 1) % len(points)]
        G.add_edge(from_point_index, to_point_index)

        from_point = points[from_point_index]
        to_point = points[to_point_index]
        distances.append(math.sqrt((to_point[0] - from_point[0])**2 + (to_point[1] - from_point[1])**2))

    pos = {i: point for i, point in enumerate(points)}

    return G, pos, sum(distances)


def get_cell_label_map(points):
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


def get_adjacencies(cell_label_map):
    adjacencies = []
    num_cells = len(cell_label_map)
    num_points = int(math.sqrt(num_cells))
    for c in range(num_cells):
        row, col = cell_label_map[c]
        conn = [0 for _ in range(num_cells)]
        for c2 in range(num_cells):
            row2, col2 = cell_label_map[c2]
            if row2 == row or col2 == col or col2 == ((col-1) % num_points) or col2 == ((col+1) % num_points):
                conn[c2] = 1
        adjacencies.append(conn)
    return adjacencies

#############

points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]

distances = get_distances(points)
# print(distances)
# >> [(0, 1, 0.5503635162326805), (0, 2, 0.6425729530566938), (0, 3, 0.35114099732158877), (1, 2, 0.45803929962395146), (1, 3, 0.39293765408777004), (2, 3, 0.291547594742265)]

distances_map = get_distances_map(distances)
# print(distances_map)
# >> {(0, 1): 0.5503635162326805, (1, 0): 0.5503635162326805, (0, 0): 0.0, (1, 1): 0.0, (0, 2): 0.6425729530566938, (2, 0): 0.6425729530566938, (2, 2): 0.0, (0, 3): 0.35114099732158877, (3, 0): 0.35114099732158877, (3, 3): 0.0, (1, 2): 0.45803929962395146, (2, 1): 0.45803929962395146, (1, 3): 0.39293765408777004, (3, 1): 0.39293765408777004, (2, 3): 0.291547594742265, (3, 2): 0.291547594742265}

activities = [
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1],
    [1,0,0,0]
]

G, pos, tour_length = get_tour_graph(points, activities)
# print(points)
# print(activities)
# print(G.nodes)
# print(G.edges)
# print(pos)
# print(tour_length)
# >> [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]
# >> [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]]
# >> [0, 1, 2, 3]
# >> [(0, 1), (0, 3), (1, 2), (2, 3)]
# >> {0: (0, 1), 1: (0.23, 0.5), 2: (0.6, 0.77), 3: (0.33, 0.88)}
# >> 1.651091407920486

# nx.draw_networkx(G, pos)
# plt.show()

clm = get_cell_label_map(points)
# print(clm)
# >> {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3), 4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (1, 3), 8: (2, 0), 9: (2, 1), 10: (2, 2), 11: (2, 3), 12: (3, 0), 13: (3, 1), 14: (3, 2), 15: (3, 3)}

adj = get_adjacencies(clm)
# print(adj)
# >> [[1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1], [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1], [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1], [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1], [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1]]
