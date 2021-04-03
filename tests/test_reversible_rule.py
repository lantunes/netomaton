from netomaton.topology import adjacency
import netomaton.rules as rules
from netomaton import ReversibleRule_2, evolve_2
from .rule_test import *


class TestReversibleRule(RuleTest):

    def test_rule150R_simple_init(self):
        expected = self._convert_to_matrix("rule150R_simple_init.ca")
        actual = self._evolve_reversible_ca(expected, 150)
        np.testing.assert_equal(expected, actual)


    @staticmethod
    def _evolve_reversible_ca(expected, rule_number):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacency_matrix = adjacency.cellular_automaton(n=size, r=1)
        r = ReversibleRule_2(rules.nks_ca_rule_2(rule_number))
        activities, adjacencies = evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                           activity_rule=r, past_conditions=[initial_conditions], timesteps=rows)
        return activities
