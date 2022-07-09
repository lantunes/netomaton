from netomaton.topology import cellular_automaton2d
import netomaton.rules as rules
from netomaton import evolve, get_activities_over_time_as_list
from .rule_test import *


class TestWireworldRule(RuleTest):

    def test_wireworld_diodes(self):
        expected = self._convert_to_matrix2d("wireworld_diodes.ca")
        actual = self._evolve_wireworld(expected)
        np.testing.assert_equal(expected, actual)

    def test_wireworld_diodes_memoized(self):
        expected = self._convert_to_matrix2d("wireworld_diodes.ca")
        actual = self._evolve_wireworld(expected, memoize=True)
        np.testing.assert_equal(expected, actual)

    def test_wireworld_xor(self):
        expected = self._convert_to_matrix2d("wireworld_xor.ca")
        actual = self._evolve_wireworld(expected)
        np.testing.assert_equal(expected, actual)

    def test_wireworld_xor_memoized(self):
        expected = self._convert_to_matrix2d("wireworld_xor.ca")
        actual = self._evolve_wireworld(expected, memoize=True)
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_wireworld(expected, memoize=False):
        steps, rows, size = expected.shape
        initial_conditions = np.array(expected[0]).reshape(rows * size).flatten()
        network = cellular_automaton2d(rows=rows, cols=size, neighbourhood="Moore")
        trajectory = evolve(initial_conditions=initial_conditions, network=network, timesteps=steps,
                            activity_rule=rules.wireworld_rule, memoize=memoize)
        activities = get_activities_over_time_as_list(trajectory)
        return np.array(activities).reshape((steps, rows, size))
