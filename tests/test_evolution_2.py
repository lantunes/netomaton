import unittest

import netomaton as ntm


class TestFunctions2(unittest.TestCase):

    def test_copy_connectivity_map(self):

        conn_map = {
            0: {0: 1.0000003, 2: 0.54534, 4: 1.0},
            1: {1: 0.23542356465, 4: 1.0},
            2: {2: 3.4546547675787688678, 7: 1.043435},
            3: {3: 1.0},
            4: {4: 1.0},
            5: {5: 1.0},
            6: {6: 1.0, 3: 9.3243242},
            7: {7: 1.10},
            8: {},
            "a": {"a": 1.0}
        }

        conn_map_copy = ntm.copy_connectivity_map(conn_map)

        self.assertEqual(conn_map, conn_map_copy)

        conn_map[3][5] = 1.0

        self.assertNotEqual(conn_map, conn_map_copy)

    def test_copy_connectivity_map_weighted_hypergraph(self):
        conn_map = {
            1: {3: (1.0, "a3")},
            2: {1: (1.35543, "a1")},
            3: {2: (1.0, "a2")},
            4: {2: (1.0, "a4"), 3: (1.0, "a4")},
            5: {2: (1.0, "a4"), 3: (10.0, "a4")},
            6: {3: (1.0, "a5"), 5: (0.03432434, "a5")}
        }

        conn_map_copy = ntm.copy_connectivity_map(conn_map)

        self.assertEqual(conn_map, conn_map_copy)

        conn_map[3][5] = (1.0, "a6")

        self.assertNotEqual(conn_map, conn_map_copy)
