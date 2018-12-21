from .rule_test import *
from netomaton import *


class TestReversibleRule(RuleTest):

    def test_rule150R_simple_init(self):
        expected = self._convert_to_matrix("rule150R_simple_init.ca")
        actual = self._evolve_reversible_ca(expected, 150)
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_reversible_ca(expected, rule_number):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacencies = AdjacencyMatrix.cellular_automaton(n=size, r=1)
        r = ReversibleRule(initial_conditions, lambda n, c, t: ActivityRule.nks_ca_rule(n, c, rule_number))
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=rows,
                                            activity_rule=r.activity_rule)
        return activities
