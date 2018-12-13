import unittest

from netomaton import *


class TestAdjacencyMatrix(unittest.TestCase):

    def test_n3_r1_ca(self):
        matrix = AdjacencyMatrix.cellular_automaton(n=3)
        expected = [[1., 1., 1.],
                    [1., 1., 1.],
                    [1., 1., 1.]]
        self.assertEqual(expected, matrix)

    def test_n5_r1_ca(self):
        matrix = AdjacencyMatrix.cellular_automaton(n=5)
        expected = [[1., 1., 0., 0., 1.],
                    [1., 1., 1., 0., 0.],
                    [0., 1., 1., 1., 0.],
                    [0., 0., 1., 1., 1.],
                    [1., 0., 0., 1., 1.]]
        self.assertEqual(expected, matrix)

    def test_n5_r2_ca(self):
        matrix = AdjacencyMatrix.cellular_automaton(n=5, r=2)
        expected = [[1., 1., 1., 1., 1.],
                    [1., 1., 1., 1., 1.],
                    [1., 1., 1., 1., 1.],
                    [1., 1., 1., 1., 1.],
                    [1., 1., 1., 1., 1.]]
        self.assertEqual(expected, matrix)

    def test_n7_r2_ca(self):
        matrix = AdjacencyMatrix.cellular_automaton(n=7, r=2)
        expected = [[1., 1., 1., 0., 0., 1., 1.],
                    [1., 1., 1., 1., 0., 0., 1.],
                    [1., 1., 1., 1., 1., 0., 0.],
                    [0., 1., 1., 1., 1., 1., 0.],
                    [0., 0., 1., 1., 1., 1., 1.],
                    [1., 0., 0., 1., 1., 1., 1.],
                    [1., 1., 0., 0., 1., 1., 1.]]
        self.assertEqual(expected, matrix)