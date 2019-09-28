import unittest

import numpy as np

import netomaton as ntm


class TestFunctions(unittest.TestCase):

    def test_neighbourhood(self):
        adjacency_matrix = [[1., .9, 0., 0., 1.],
                       [1., 1., 1., 0., 0.],
                       [0., 1., 1., 1., 0.],
                       [0., 0., 1., 1., 1.],
                       [1., 0., 0., 1., .8]]

        initial_conditions = [2., 3., 4., 5., 6.]

        def evaluate_neighbourhoods(ctx):
            c = ctx.node_index
            if c == 0:
                np.testing.assert_equal([2., 3., 6.], ctx.activities)
                np.testing.assert_equal([0, 1, 4], ctx.neighbour_indices)
                np.testing.assert_equal([1., 1., 1.], ctx.weights)
            elif c == 1:
                np.testing.assert_equal([2., 3., 4.], ctx.activities)
                np.testing.assert_equal([0, 1, 2], ctx.neighbour_indices)
                np.testing.assert_equal([.9, 1., 1.], ctx.weights)
            elif c == 2:
                np.testing.assert_equal([3., 4., 5.], ctx.activities)
                np.testing.assert_equal([1, 2, 3], ctx.neighbour_indices)
                np.testing.assert_equal([1., 1., 1.], ctx.weights)
            elif c == 3:
                np.testing.assert_equal([4., 5., 6.], ctx.activities)
                np.testing.assert_equal([2, 3, 4], ctx.neighbour_indices)
                np.testing.assert_equal([1., 1., 1.], ctx.weights)
            elif c == 4:
                np.testing.assert_equal([2., 5., 6.], ctx.activities)
                np.testing.assert_equal([0, 3, 4], ctx.neighbour_indices)
                np.testing.assert_equal([1., 1., .8], ctx.weights)

        ntm.evolve(initial_conditions, adjacency_matrix, timesteps=2, activity_rule=evaluate_neighbourhoods)

    def test_init_simple_1(self):
        arr = ntm.init_simple(1)
        self.assertEqual(len(arr), 1)
        self.assertEqual(arr[0], 1)

    def test_init_simple_1_val2(self):
        arr = ntm.init_simple(1, val=2)
        self.assertEqual(len(arr), 1)
        self.assertEqual(arr[0], 2)

    def test_init_simple_3(self):
        arr = ntm.init_simple(3)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], 0)
        self.assertEqual(arr[1], 1)
        self.assertEqual(arr[2], 0)
        
    def test_init_random_3(self):
        arr = ntm.init_random(3, empty_value=9)
        self.assertEqual(len(arr), 3)
        self.assertTrue(0 <= arr[0] <= 1)
        self.assertTrue(0 <= arr[1] <= 1)
        self.assertTrue(0 <= arr[2] <= 1)

    def test_init_random_3_k3(self):
        arr = ntm.init_random(3, k=3, empty_value=9)
        self.assertEqual(len(arr), 3)
        self.assertTrue(0 <= arr[0] <= 2)
        self.assertTrue(0 <= arr[1] <= 2)
        self.assertTrue(0 <= arr[2] <= 2)

    def test_init_random_3_k3_n1(self):
        arr = ntm.init_random(3, k=3, n_randomized=1, empty_value=9)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], 9)
        self.assertTrue(0 <= arr[1] <= 2)
        self.assertEqual(arr[2], 9)

    def test_init_random_3_k3_n0(self):
        arr = ntm.init_random(3, k=3, n_randomized=0, empty_value=9)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], 9)
        self.assertEqual(arr[1], 9)
        self.assertEqual(arr[2], 9)

    def test_init_random_3_k3_n3(self):
        arr = ntm.init_random(3, k=3, n_randomized=3, empty_value=9)
        self.assertEqual(len(arr), 3)
        self.assertTrue(0 <= arr[0] <= 2)
        self.assertTrue(0 <= arr[1] <= 2)
        self.assertTrue(0 <= arr[2] <= 2)

    def test_init_random_3_k3_n2(self):
        arr = ntm.init_random(3, k=3, n_randomized=2, empty_value=9)
        self.assertEqual(len(arr), 3)
        self.assertTrue(0 <= arr[0] <= 2)
        self.assertTrue(0 <= arr[1] <= 2)
        self.assertEqual(arr[2], 9)

    def test_init_random_1_k3_n1(self):
        arr = ntm.init_random(1, k=3, n_randomized=1, empty_value=9)
        self.assertEqual(len(arr), 1)
        self.assertTrue(0 <= arr[0] <= 2)

    def test_init_random_1_k3_n0(self):
        arr = ntm.init_random(1, k=3, n_randomized=0, empty_value=9)
        self.assertEqual(len(arr), 1)
        self.assertEqual(arr[0], 9)

    def test_init_simple2d_1x1(self):
        arr = ntm.init_simple2d(rows=1, cols=1)
        self.assertEqual(len(arr), 1)
        self.assertEqual(arr[0], 1)

    def test_init_simple2d_1x1_val2(self):
        arr = ntm.init_simple2d(rows=1, cols=1, val=2)
        self.assertEqual(len(arr), 1)
        self.assertEqual(arr[0], 2)

    def test_init_simple2d_2x2(self):
        arr = ntm.init_simple2d(rows=2, cols=2)
        self.assertEqual(len(arr), 4)
        self.assertEqual(arr, [0, 0, 0, 1])

    def test_init_simple2d_3x3(self):
        arr = ntm.init_simple2d(rows=3, cols=3)
        self.assertEqual(len(arr), 9)
        self.assertEqual(arr, [0, 0, 0, 0, 1, 0, 0, 0, 0])

    def test_init_simple2d_2x3(self):
        arr = ntm.init_simple2d(rows=2, cols=3)
        self.assertEqual(len(arr), 6)
        self.assertEqual(arr, [0, 0, 0, 0, 1, 0])

    def test_past_activities_single_past(self):
        adjacency_matrix = [
            [1, 1],
            [1, 1]
        ]

        initial_conditions = [1, 1]

        past_conditions = [
            [0, 0]
        ]

        def activity_rule(ctx):
            p = ctx.past_activities
            t = ctx.timestep
            if t == 1:
                self.assertEqual(p, [[0, 0]])
            if t == 2:
                self.assertEqual(p, [[1, 1]])
            if t == 3:
                self.assertEqual(p, [[2, 2]])
            return ctx.current_activity + 1

        activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, activity_rule, timesteps=4,
                                   past_conditions=past_conditions)

        np.testing.assert_equal(activities, [
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4]
        ])

    def test_past_activities_multiple_past(self):
        adjacency_matrix = [
            [1, 1],
            [1, 1]
        ]

        initial_conditions = [1, 1]

        past_conditions = [
            [-1, -1],
            [0, 0]
        ]

        def activity_rule(ctx):
            p = ctx.past_activities
            t = ctx.timestep
            if t == 1:
                self.assertEqual(p, [
                    [-1, -1],
                    [0, 0]
                ])
            if t == 2:
                self.assertEqual(p, [
                    [0, 0],
                    [1, 1]
                ])
            if t == 3:
                self.assertEqual(p, [
                    [1, 1],
                    [2, 2]
                ])
            return ctx.current_activity + 1

        activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, activity_rule, timesteps=4,
                                   past_conditions=past_conditions)

        np.testing.assert_equal(activities, [
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4]
        ])
