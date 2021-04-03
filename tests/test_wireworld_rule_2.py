from netomaton.topology import adjacency
import netomaton.rules as rules
from netomaton import evolve_2
from .rule_test import *


class TestWireworldRule(RuleTest):

    def test_wireworld_diodes(self):
        expected = self._convert_to_matrix2d("wireworld_diodes.ca")
        actual = self._evolve_wireworld(expected)
        np.testing.assert_equal(expected, actual)

    def test_wireworld_xor(self):
        expected = self._convert_to_matrix2d("wireworld_xor.ca")
        actual = self._evolve_wireworld(expected)
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_wireworld(expected):
        steps, rows, size = expected.shape
        initial_conditions = np.array(expected[0]).reshape(rows * size).flatten()
        adjacency_matrix = adjacency.cellular_automaton2d(rows=rows, cols=size, neighbourhood="Moore")
        activities, _ = evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=steps,
                                 activity_rule=rules.wireworld_rule_2)
        return np.array(activities).reshape((steps, rows, size))
