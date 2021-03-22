import netomaton.network as adjacency
import netomaton.rules as rules
from netomaton import NodeContext_2, evolve_2
from .rule_test import *


class TestRules(RuleTest):

    def test_majority_rule(self):
        actual = rules.majority_rule_2(NodeContext_2(0, 1, {}, [0, 1, 2, 3, 4], [1, 2, 1, 3, 4], [1., 1., 1., 1., 1.], 0, None, None))
        expected = 1
        self.assertEqual(expected, actual)

        actual = rules.majority_rule_2(NodeContext_2(0, 1, {}, [0, 1, 2, 3, 4], [2, 2, 2, 2, 2], [1., 1., 1., 1., 1.], 0, None, None))
        expected = 2
        self.assertEqual(expected, actual)

        actual = rules.majority_rule_2(NodeContext_2(0, 1, {}, [0], [3], [1.], 0, None, None))
        expected = 3
        self.assertEqual(expected, actual)

        actual = rules.majority_rule_2(NodeContext_2(0, 1, {}, [0, 1, 2], [0., 0., 5423.], [1., 1., 1.], 0, None, None))
        expected = 0.
        self.assertEqual(expected, actual)

    def test_rule0_simple_init(self):
        expected = self._convert_to_matrix("rule0_simple_init.ca")
        actual = self._evolve_nks_ca(expected, 0)
        np.testing.assert_equal(expected, actual)

    def test_rule0_random_init(self):
        expected = self._convert_to_matrix("rule0_random_init.ca")
        actual = self._evolve_nks_ca(expected, 0)
        np.testing.assert_equal(expected, actual)

    def test_nks_ca_rule30_simple_init(self):
        expected_activities = self._convert_to_matrix("rule30_simple_init.ca")
        actual_activities = self._evolve_nks_ca(expected_activities, 30)
        np.testing.assert_equal(expected_activities, actual_activities)

    def test_nks_ca_rule30_random_init(self):
        expected_activities = self._convert_to_matrix("rule30_random_init.ca")
        actual_activities = self._evolve_nks_ca(expected_activities, 30)
        np.testing.assert_equal(expected_activities, actual_activities)

    def test_rule126_simple_init(self):
        expected = self._convert_to_matrix("rule126_simple_init.ca")
        actual = self._evolve_nks_ca(expected, 126)
        np.testing.assert_equal(expected, actual)

    def test_rule126_random_init(self):
        expected = self._convert_to_matrix("rule126_random_init.ca")
        actual = self._evolve_nks_ca(expected, 126)
        np.testing.assert_equal(expected, actual)

    def test_rule225_simple_init(self):
        expected = self._convert_to_matrix("rule225_simple_init.ca")
        actual = self._evolve_nks_ca(expected, 225)
        np.testing.assert_equal(expected, actual)

    def test_rule225_random_init(self):
        expected = self._convert_to_matrix("rule225_random_init.ca")
        actual = self._evolve_nks_ca(expected, 225)
        np.testing.assert_equal(expected, actual)

    def test_rule255_simple_init(self):
        expected = self._convert_to_matrix("rule255_simple_init.ca")
        actual = self._evolve_nks_ca(expected, 255)
        np.testing.assert_equal(expected, actual)

    def test_rule255_random_init(self):
        expected = self._convert_to_matrix("rule255_random_init.ca")
        actual = self._evolve_nks_ca(expected, 255)
        np.testing.assert_equal(expected, actual)

    def test_totalistic_3color_rule777_simple_init(self):
        expected = self._convert_to_matrix("tot3_rule777_simple_init.ca")
        actual = self._evolve_totalistic_ca(expected, 3, 777)
        np.testing.assert_equal(expected, actual)

    def test_totalistic_3color_rule777_random_init(self):
        expected = self._convert_to_matrix("tot3_rule777_random_init.ca")
        actual = self._evolve_totalistic_ca(expected, 3, 777)
        np.testing.assert_equal(expected, actual)

    def test_totalistic_4color_rule107396_simple_init(self):
        expected = self._convert_to_matrix("tot4_rule107396_simple_init.ca")
        actual = self._evolve_totalistic_ca(expected, 4, 107396)
        np.testing.assert_equal(expected, actual)

    def test_totalistic_4color_rule107396_random_init(self):
        expected = self._convert_to_matrix("tot4_rule107396_random_init.ca")
        actual = self._evolve_totalistic_ca(expected, 4, 107396)
        np.testing.assert_equal(expected, actual)

    def test_shift_to_center(self):
        activities = [1, 1, 0]
        node_indices = [0, 1, 199]
        node_index = 0
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([0, 1, 1], shifted)

        activities = [1, 1, 0]
        node_indices = [0, 1, 199]
        node_index = 1
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([1, 1, 0], shifted)

        activities = [1, 1, 0]
        node_indices = [0, 1, 199]
        node_index = 199
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([1, 0, 1], shifted)

        activities = [1, 2, 3, 4, 5]
        node_indices = [0, 1, 2, 198, 199]
        node_index = 0
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([4, 5, 1, 2, 3], shifted)

        activities = [1, 2, 3, 4, 5]
        node_indices = [0, 1, 2, 198, 199]
        node_index = 1
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([5, 1, 2, 3, 4], shifted)

        activities = [1, 2, 3, 4, 5]
        node_indices = [0, 1, 2, 198, 199]
        node_index = 2
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([1, 2, 3, 4, 5], shifted)

        activities = [1, 2, 3, 4, 5]
        node_indices = [0, 1, 2, 198, 199]
        node_index = 198
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([2, 3, 4, 5, 1], shifted)

        activities = [1, 2, 3, 4, 5]
        node_indices = [0, 1, 2, 198, 199]
        node_index = 199
        shifted = rules.shift_to_center(activities, node_indices, node_index)
        self.assertEqual([3, 4, 5, 1, 2], shifted)

    def test_ca_density_classification(self):
        expected = self._convert_to_matrix("ca_density_classification.ca")
        actual = self._evolve_binary_ca(expected, r=3, rule=6667021275756174439087127638698866559)
        np.testing.assert_equal(expected, actual)

    def test_tot_rule126_2d_n9_simple_init(self):
        expected = self._convert_to_matrix2d("tot_rule126_2d_n9_simple_init.ca")
        actual = self._evolve_totalistic_ca2d(expected, 126, 'Moore')
        np.testing.assert_equal(expected, actual)

    def test_tot_rule26_2d_n5_simple_init(self):
        expected = self._convert_to_matrix2d("tot_rule26_2d_n5_simple_init.ca")
        actual = self._evolve_totalistic_ca2d(expected, 26, 'von Neumann')
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_nks_ca(expected, rule):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacency_matrix = adjacency.cellular_automaton(n=size, r=1)
        activities, adjacencies = evolve_2(initial_conditions, adjacency_matrix, timesteps=rows,
                                           activity_rule=rules.nks_ca_rule_2(rule))
        return activities

    @staticmethod
    def _evolve_binary_ca(expected, r, rule):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacency_matrix = adjacency.cellular_automaton(n=size, r=r)
        activities, adjacencies = evolve_2(initial_conditions, adjacency_matrix, timesteps=rows,
                                           activity_rule=rules.binary_ca_rule_2(rule))
        return activities

    @staticmethod
    def _evolve_totalistic_ca(expected, k, rule):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacency_matrix = adjacency.cellular_automaton(n=size, r=1)
        activities, adjacencies = evolve_2(initial_conditions, adjacency_matrix, timesteps=rows,
                                           activity_rule=rules.totalistic_ca_2(k, rule))
        return activities

    @staticmethod
    def _evolve_totalistic_ca2d(expected, rule, neighbourhood):
        steps, rows, size = expected.shape
        initial_conditions = np.array(expected[0]).reshape(rows * size).flatten()
        adjacency_matrix = adjacency.cellular_automaton2d(rows=rows, cols=size, r=1, neighbourhood=neighbourhood)
        activities, adjacencies = evolve_2(initial_conditions, adjacency_matrix, timesteps=steps,
                                           activity_rule=rules.totalistic_ca_2(k=2, rule=rule))
        return np.array(activities).reshape((steps, rows, size))
