import netomaton.network as AdjacencyMatrix
from netomaton import ActivityRule, Neighbourhood, evolve
from .rule_test import *


class TestActivityRule(RuleTest):

    def test_majority_rule(self):
        actual = ActivityRule.majority_rule(Neighbourhood([1, 2, 1, 3, 4], [0, 1, 2, 3, 4], [1., 1., 1., 1., 1.], 0))
        expected = 1
        self.assertEqual(expected, actual)

        actual = ActivityRule.majority_rule(Neighbourhood([2, 2, 2, 2, 2], [0, 1, 2, 3, 4], [1., 1., 1., 1., 1.], 0))
        expected = 2
        self.assertEqual(expected, actual)

        actual = ActivityRule.majority_rule(Neighbourhood([3], [0], [1.], 0))
        expected = 3
        self.assertEqual(expected, actual)

        actual = ActivityRule.majority_rule(Neighbourhood([0., 0., 5423.], [0, 1, 2], [1., 1., 1.], 0))
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
        cell_indices = [0, 1, 199]
        cell_index = 0
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([0, 1, 1], shifted)

        activities = [1, 1, 0]
        cell_indices = [0, 1, 199]
        cell_index = 1
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([1, 1, 0], shifted)

        activities = [1, 1, 0]
        cell_indices = [0, 1, 199]
        cell_index = 199
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([1, 0, 1], shifted)

        activities = [1, 2, 3, 4, 5]
        cell_indices = [0, 1, 2, 198, 199]
        cell_index = 0
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([4, 5, 1, 2, 3], shifted)

        activities = [1, 2, 3, 4, 5]
        cell_indices = [0, 1, 2, 198, 199]
        cell_index = 1
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([5, 1, 2, 3, 4], shifted)

        activities = [1, 2, 3, 4, 5]
        cell_indices = [0, 1, 2, 198, 199]
        cell_index = 2
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([1, 2, 3, 4, 5], shifted)

        activities = [1, 2, 3, 4, 5]
        cell_indices = [0, 1, 2, 198, 199]
        cell_index = 198
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([2, 3, 4, 5, 1], shifted)

        activities = [1, 2, 3, 4, 5]
        cell_indices = [0, 1, 2, 198, 199]
        cell_index = 199
        shifted = ActivityRule.shift_to_center(activities, cell_indices, cell_index)
        self.assertEquals([3, 4, 5, 1, 2], shifted)

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
        adjacencies = AdjacencyMatrix.cellular_automaton(n=size, r=1)
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=rows,
                                            activity_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, rule))
        return activities

    @staticmethod
    def _evolve_binary_ca(expected, r, rule):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacencies = AdjacencyMatrix.cellular_automaton(n=size, r=r)
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=rows,
                                            activity_rule=lambda n, c, t: ActivityRule.binary_ca_rule(n, c, rule))
        return activities

    @staticmethod
    def _evolve_totalistic_ca(expected, k, rule):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacencies = AdjacencyMatrix.cellular_automaton(n=size, r=1)
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=rows,
                                            activity_rule=lambda n, c, t: ActivityRule.totalistic_ca(n, k, rule))
        return activities

    @staticmethod
    def _evolve_totalistic_ca2d(expected, rule, neighbourhood):
        steps, rows, size = expected.shape
        initial_conditions = np.array(expected[0]).reshape(rows * size).flatten()
        adjacencies = AdjacencyMatrix.cellular_automaton2d(rows=rows, cols=size, r=1, neighbourhood=neighbourhood)
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=steps,
                                            activity_rule=lambda n, c, t: ActivityRule.totalistic_ca(n, k=2, rule=rule))
        return np.array(activities).reshape((steps, rows, size))
