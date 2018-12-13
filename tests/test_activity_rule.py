import unittest

from netomaton import *

import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestActivityRule(unittest.TestCase):

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

    def test_sequential_left_to_right(self):
        expected = self._convert_to_matrix("rule60_sequential_simple_init.ca")
        adjacencies = AdjacencyMatrix.cellular_automaton(n=21)
        initial_conditions = [0]*10 + [1] + [0]*10
        r = AsynchronousRule(apply_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 60), update_order=range(1, 20))
        activities, connectivities = evolve(adjacencies, initial_conditions, timesteps=19*20,
                                            activity_rule=r.activity_rule)
        np.testing.assert_equal(expected, activities[::19])

    def test_sequential_random(self):
        expected = self._convert_to_matrix("rule90_sequential_simple_init.ca")
        adjacencies = AdjacencyMatrix.cellular_automaton(n=21)
        initial_conditions = [0]*10 + [1] + [0]*10
        update_order = [19, 11, 4, 9, 6, 16, 10, 2, 17, 1, 12, 15, 5, 3, 8, 18, 7, 13, 14]
        r = AsynchronousRule(apply_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 90), update_order=update_order)
        activities, connectivities = evolve(adjacencies, initial_conditions, timesteps=19*20,
                                            activity_rule=r.activity_rule)
        np.testing.assert_equal(expected, activities[::19])

    def test_ca_density_classification(self):
        expected = self._convert_to_matrix("ca_density_classification.ca")
        actual = self._evolve_binary_ca(expected, r=3, rule=6667021275756174439087127638698866559)
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _convert_to_matrix(filename):
        with open(os.path.join(THIS_DIR, 'resources', filename), 'r') as content_file:
            content = content_file.read()
        content = content.replace('{{', '')
        content = content.replace('}}', '')
        content = content.replace('{', '')
        content = content.replace('},', ';')
        return np.matrix(content, dtype=np.int).tolist()

    @staticmethod
    def _evolve_nks_ca(expected, rule):
        rows, size = len(expected), len(expected[0])
        initial_conditions = expected[0]
        adjacencies = AdjacencyMatrix.cellular_automaton(n=size, r=1)
        activities, connectivities = evolve(adjacencies, initial_conditions, timesteps=rows,
                                            activity_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, rule))
        return activities

    @staticmethod
    def _evolve_binary_ca(expected, r, rule):
        rows, size = len(expected), len(expected[0])
        initial_conditions = expected[0]
        adjacencies = AdjacencyMatrix.cellular_automaton(n=size, r=r)
        activities, connectivities = evolve(adjacencies, initial_conditions, timesteps=rows,
                                            activity_rule=lambda n, c, t: ActivityRule.binary_ca_rule(n, c, rule))
        return activities

    @staticmethod
    def _evolve_totalistic_ca(expected, k, rule):
        rows, size = len(expected), len(expected[0])
        initial_conditions = expected[0]
        adjacencies = AdjacencyMatrix.cellular_automaton(n=size, r=1)
        activities, connectivities = evolve(adjacencies, initial_conditions, timesteps=rows,
                                            activity_rule=lambda n, c, t: ActivityRule.totalistic_ca(n, k, rule))
        return activities
