import unittest

from netomaton import *


class TestFunctions(unittest.TestCase):

    def test_neighbourhood(self):
        adjacencies = [[1., .9, 0., 0., 1.],
                       [1., 1., 1., 0., 0.],
                       [0., 1., 1., 1., 0.],
                       [0., 0., 1., 1., 1.],
                       [1., 0., 0., 1., .8]]

        initial_conditions = [2., 3., 4., 5., 6.]

        def evaluate_neighbourhoods(n, c, t):
            if c == 0:
                self.assertEqual([2., 3., 6.], n.activities)
                self.assertEqual([0, 1, 4], n.neighbour_indices)
                self.assertEqual([1., 1., 1.], n.weights)
            elif c == 1:
                self.assertEqual([2., 3., 4.], n.activities)
                self.assertEqual([0, 1, 2], n.neighbour_indices)
                self.assertEqual([.9, 1., 1.], n.weights)
            elif c == 2:
                self.assertEqual([3., 4., 5.], n.activities)
                self.assertEqual([1, 2, 3], n.neighbour_indices)
                self.assertEqual([1., 1., 1.], n.weights)
            elif c == 3:
                self.assertEqual([4., 5., 6.], n.activities)
                self.assertEqual([2, 3, 4], n.neighbour_indices)
                self.assertEqual([1., 1., 1.], n.weights)
            elif c == 4:
                self.assertEqual([2., 5., 6.], n.activities)
                self.assertEqual([0, 3, 4], n.neighbour_indices)
                self.assertEqual([1., 1., .8], n.weights)

        evolve(adjacencies, initial_conditions, timesteps=2, activity_rule=evaluate_neighbourhoods)
