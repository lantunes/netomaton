import unittest
import netomaton as ntm


class TestUtils(unittest.TestCase):

    def test_get_node_degrees(self):
        connectivity_map = {
            0: {1: [{}], 2: [{}]},
            1: {0: [{}]},
            2: {0: [{}], 1: [{}], 2: [{}]}
        }

        in_degrees, out_degrees = ntm.get_node_degrees(connectivity_map)

        self.assertEqual({0: 2, 1: 1, 2: 3}, in_degrees)
        self.assertEqual({0: 2, 1: 2, 2: 2}, out_degrees)

    def test_get_node_degrees_multi(self):
        connectivity_map = {
            0: {1: [{}], 2: [{}, {}]},
            1: {},
            2: {0: [{}, {}, {}], 2: [{}]}
        }

        in_degrees, out_degrees = ntm.get_node_degrees(connectivity_map)

        self.assertEqual({0: 3, 1: 0, 2: 4}, in_degrees)
        self.assertEqual({0: 3, 1: 1, 2: 3}, out_degrees)
