import unittest
import numpy as np
import netomaton as ntm


class TestFunctions(unittest.TestCase):

    def test_neighbourhood(self):
        network = ntm.topology.from_adjacency_matrix([
           [1.0, 0.9, 0.0, 0.0, 1.0],
           [1.0, 1.0, 1.0, 0.0, 0.0],
           [0.0, 1.0, 1.0, 1.0, 0.0],
           [0.0, 0.0, 1.0, 1.0, 1.0],
           [1.0, 0.0, 0.0, 1.0, 0.8]
        ])

        initial_conditions = [2., 3., 4., 5., 6.]

        def evaluate_neighbourhoods(ctx):
            c = ctx.node_label
            if c == 0:
                np.testing.assert_equal([2., 3., 6.], ctx.neighbourhood_activities)
                np.testing.assert_equal([0, 1, 4], ctx.neighbour_labels)
                np.testing.assert_equal({0: [{'weight': 1.0}], 1: [{'weight': 1.0}], 4: [{'weight': 1.0}]},
                                        ctx.connection_states)
            elif c == 1:
                np.testing.assert_equal([2., 3., 4.], ctx.neighbourhood_activities)
                np.testing.assert_equal([0, 1, 2], ctx.neighbour_labels)
                np.testing.assert_equal({0: [{'weight': .9}], 1: [{'weight': 1.0}], 2: [{'weight': 1.0}]},
                                        ctx.connection_states)
            elif c == 2:
                np.testing.assert_equal([3., 4., 5.], ctx.neighbourhood_activities)
                np.testing.assert_equal([1, 2, 3], ctx.neighbour_labels)
                np.testing.assert_equal({1: [{'weight': 1.0}], 2: [{'weight': 1.0}], 3: [{'weight': 1.0}]},
                                        ctx.connection_states)
            elif c == 3:
                np.testing.assert_equal([4., 5., 6.], ctx.neighbourhood_activities)
                np.testing.assert_equal([2, 3, 4], ctx.neighbour_labels)
                np.testing.assert_equal({2: [{'weight': 1.0}], 3: [{'weight': 1.0}], 4: [{'weight': 1.0}]},
                                        ctx.connection_states)
            elif c == 4:
                np.testing.assert_equal([2., 5., 6.], ctx.neighbourhood_activities)
                np.testing.assert_equal([0, 3, 4], ctx.neighbour_labels)
                np.testing.assert_equal({0: [{'weight': 1.0}], 3: [{'weight': 1.0}], 4: [{'weight': .8}]},
                                        ctx.connection_states)

        ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=2,
                   activity_rule=evaluate_neighbourhoods)

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
        network = ntm.topology.from_adjacency_matrix([
            [1, 1],
            [1, 1]
        ])

        initial_conditions = [1, 1]

        past_conditions = [
            [0, 0]
        ]

        def activity_rule(ctx):
            p = ctx.past_activities
            t = ctx.timestep
            if t == 1:
                self.assertEqual(p, [{0: 0, 1: 0}])
            if t == 2:
                self.assertEqual(p, [{0: 1, 1: 1}])
            if t == 3:
                self.assertEqual(p, [{0: 2, 1: 2}])
            return ctx.current_activity + 1

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                                activity_rule=activity_rule, timesteps=4, past_conditions=past_conditions)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        np.testing.assert_equal(activities, [
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4]
        ])

    def test_past_activities_multiple_past(self):
        network = ntm.topology.from_adjacency_matrix([
            [1, 1],
            [1, 1]
        ])

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
                    {0: -1, 1: -1},
                    {0: 0, 1: 0}
                ])
            if t == 2:
                self.assertEqual(p, [
                    {0: 0, 1: 0},
                    {0: 1, 1: 1}
                ])
            if t == 3:
                self.assertEqual(p, [
                    {0: 1, 1: 1},
                    {0: 2, 1: 2}
                ])
            return ctx.current_activity + 1

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                                activity_rule=activity_rule, timesteps=4, past_conditions=past_conditions)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        np.testing.assert_equal(activities, [
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4]
        ])

    def test_persist_activities_true(self):
        network = ntm.topology.from_adjacency_matrix([[1]])
        initial_conditions = {0: 1}

        trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions,
                                activity_rule=lambda ctx: 1, timesteps=3, persist_activities=True)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        self.assertEqual([[1], [1], [1]], activities)

    def test_persist_activities_false(self):
        network = ntm.topology.from_adjacency_matrix([[1]])
        initial_conditions = {0: 1}

        trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions,
                                activity_rule=lambda ctx: 1, timesteps=3, persist_activities=False)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        self.assertEqual([[1]], activities)

    def test_persist_network_true(self):
        network = ntm.topology.from_adjacency_matrix([[1]])
        initial_conditions = {0: 1}

        trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions,
                                topology_rule=lambda ctx: ctx.network,
                                timesteps=3, persist_network=True)

        topology = [state.network.to_adjacency_matrix() for state in trajectory if state.network]
        self.assertEqual([[[1]], [[1]], [[1]]], topology)

    def test_persist_network_false(self):
        network = ntm.topology.from_adjacency_matrix([[1]])
        initial_conditions = {0: 1}

        trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions,
                                topology_rule=lambda ctx: ctx.network,
                                timesteps=3, persist_network=False)

        topology = [state.network.to_adjacency_matrix() for state in trajectory if state.network]
        self.assertEqual([[[1]]], topology)
