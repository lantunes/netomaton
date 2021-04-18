import unittest
import numpy as np
from netomaton import HopfieldTankTSPNet, evolve, topology, get_activities_over_time_as_list


class TestHopfieldTankTSPNet(unittest.TestCase):

    def test_get_distances(self):
        points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]
        tsp_net = HopfieldTankTSPNet(points)

        distances = tsp_net.get_distances()

        expected = [(0, 1, 0.5503635162326805), (0, 2, 0.6425729530566938), (0, 3, 0.35114099732158877),
                    (1, 2, 0.45803929962395146), (1, 3, 0.39293765408777004), (2, 3, 0.291547594742265)]
        self.assertEqual(expected, distances)

    def test_get_distances_map(self):
        points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]
        tsp_net = HopfieldTankTSPNet(points)

        distances = tsp_net.get_distances()
        distances_map = tsp_net._get_distances_map(distances)

        expected = {
            (0, 1): 0.5503635162326805,
            (1, 0): 0.5503635162326805,
            (0, 0): 0.0,
            (1, 1): 0.0,
            (0, 2): 0.6425729530566938,
            (2, 0): 0.6425729530566938,
            (2, 2): 0.0,
            (0, 3): 0.35114099732158877,
            (3, 0): 0.35114099732158877,
            (3, 3): 0.0,
            (1, 2): 0.45803929962395146,
            (2, 1): 0.45803929962395146,
            (1, 3): 0.39293765408777004,
            (3, 1): 0.39293765408777004,
            (2, 3): 0.291547594742265,
            (3, 2): 0.291547594742265
        }
        self.assertDictEqual(expected, distances_map)

    def test_get_tour_graph(self):
        points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]
        tsp_net = HopfieldTankTSPNet(points)

        permutation_matrix = [
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 0]
        ]
        G, pos, tour_length = tsp_net.get_tour_graph(points, permutation_matrix)

        expected_nodes = [0, 1, 2, 3]
        self.assertEqual(expected_nodes, list(G.nodes))

        expected_edges = [(0, 1), (0, 3), (1, 2), (2, 3)]
        self.assertEqual(expected_edges, list(G.edges))

        expected_pos = {0: (0, 1), 1: (0.23, 0.5), 2: (0.6, 0.77), 3: (0.33, 0.88)}
        self.assertDictEqual(expected_pos, pos)

        self.assertEqual(1.651091407920486, tour_length)

    def test_get_node_label_map(self):
        points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]
        tsp_net = HopfieldTankTSPNet(points)

        node_label_map = tsp_net._get_node_label_map(points)

        expected = {
            0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3),
            4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (1, 3),
            8: (2, 0), 9: (2, 1), 10: (2, 2), 11: (2, 3),
            12: (3, 0), 13: (3, 1), 14: (3, 2), 15: (3, 3)
        }
        self.assertDictEqual(expected, node_label_map)

    def test_get_adjacency_matrix(self):
        points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]
        tsp_net = HopfieldTankTSPNet(points)

        node_label_map = tsp_net._get_node_label_map(points)

        adjacency_matrix = tsp_net._get_adjacency_matrix(node_label_map)

        num_nodes = len(points)*len(points)
        expected = [[1 for _ in range(num_nodes)] for _ in range(num_nodes)]

        self.assertEqual(expected, adjacency_matrix)

    def test_evolution(self):
        points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88)]
        A, B, C, D, n, dt, timesteps = 120, 120, 40, 120, 5, 1e-05, 1000
        tsp_net = HopfieldTankTSPNet(points, dt=dt, A=A, B=B, C=C, D=D, n=n)

        initial_conditions = [-0.022395203920575254, -0.023184407969001723, -0.022224769264670836,
                              -0.022411201286076467, -0.02308227809621827, -0.023463757363683353,
                              -0.0222625041883513, -0.0228662974775357, -0.023547421145956916,
                              -0.02142219621197953, -0.022375730795237334, -0.022534578294732176,
                              -0.021526161923257372, -0.02003505371915011, -0.023113647911417328,
                              -0.023001396844357286]

        trajectory = evolve(initial_conditions=initial_conditions,
                            network=topology.from_adjacency_matrix(tsp_net.adjacency_matrix),
                            activity_rule=tsp_net.activity_rule, timesteps=timesteps)

        activities = get_activities_over_time_as_list(trajectory)
        permutation_matrix = tsp_net.get_permutation_matrix(activities)

        expected_permutation_matrix = [[4.81578032e-08, 0.0, 0.0, 0.0],
                                       [0.0, 0.0, 0.0, 1.0],
                                       [0.0, 0.0, 7.50011973e-01, 0.0],
                                       [0.0, 1.0, 0.0, 0.0]]
        np.testing.assert_almost_equal(expected_permutation_matrix, permutation_matrix)

        _, _, tour_length = tsp_net.get_tour_graph(points, permutation_matrix)
        self.assertEqual(1.6510914079204857, tour_length)
