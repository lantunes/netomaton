import unittest

from netomaton import topology


class TestTopology(unittest.TestCase):

    def test_cellular_automaton_rotation_system(self):
        network = topology.cellular_automaton(n=5, r=1)

        self.assertEqual(network.rotation_system, {
            0: [4, 0, 1],
            1: [0, 1, 2],
            2: [1, 2, 3],
            3: [2, 3, 4],
            4: [3, 4, 0]
        })

    def test_cellular_automaton_rotation_system_r2(self):
        network = topology.cellular_automaton(n=7, r=2)

        self.assertEqual(network.rotation_system, {
            0: [5, 6, 0, 1, 2],
            1: [6, 0, 1, 2, 3],
            2: [0, 1, 2, 3, 4],
            3: [1, 2, 3, 4, 5],
            4: [2, 3, 4, 5, 6],
            5: [3, 4, 5, 6, 0],
            6: [4, 5, 6, 0, 1]
        })

    def test_cellular_automaton2d_rotation_system_Moore(self):
        network = topology.cellular_automaton2d(3, 3, r=1, neighbourhood="Moore")

        self.assertEqual(network.rotation_system, {
            0: [5, 6, 7, 8, 0, 1, 2, 3, 4],
            1: [6, 7, 8, 0, 1, 2, 3, 4, 5],
            2: [7, 8, 0, 1, 2, 3, 4, 5, 6],
            3: [8, 0, 1, 2, 3, 4, 5, 6, 7],
            4: [0, 1, 2, 3, 4, 5, 6, 7, 8],
            5: [1, 2, 3, 4, 5, 6, 7, 8, 0],
            6: [2, 3, 4, 5, 6, 7, 8, 0, 1],
            7: [3, 4, 5, 6, 7, 8, 0, 1, 2],
            8: [4, 5, 6, 7, 8, 0, 1, 2, 3]
        })

    def test_cellular_automaton2d_rotation_system_von_Neumann(self):
        network = topology.cellular_automaton2d(3, 3, r=1, neighbourhood="von Neumann")

        self.assertEqual(network.rotation_system, {
            0: [3, 6, 0, 1, 2],
            1: [7, 0, 1, 2, 4],
            2: [0, 1, 2, 5, 8],
            3: [6, 0, 3, 4, 5],
            4: [1, 3, 4, 5, 7],
            5: [3, 4, 5, 8, 2],
            6: [0, 3, 6, 7, 8],
            7: [4, 6, 7, 8, 1],
            8: [6, 7, 8, 2, 5]
        })
