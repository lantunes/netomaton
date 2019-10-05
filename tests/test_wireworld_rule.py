import netomaton.network as network
import netomaton.rules as rules
from netomaton import evolve
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
        adjacency_matrix = network.cellular_automaton2d(rows=rows, cols=size, neighbourhood="Moore")
        activities, _ = evolve(initial_conditions, adjacency_matrix, timesteps=steps,
                               activity_rule=rules.wireworld_rule)
        return np.array(activities).reshape((steps, rows, size))
