import unittest

import netomaton as ntm


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

        ntm.evolve(initial_conditions, adjacencies, timesteps=2, activity_rule=evaluate_neighbourhoods)

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

