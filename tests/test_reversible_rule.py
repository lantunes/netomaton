import netomaton.network as adjacency
import netomaton.rules as rules
from netomaton import ReversibleRule, evolve
from .rule_test import *


class TestReversibleRule(RuleTest):

    def test_rule150R_simple_init(self):
        expected = self._convert_to_matrix("rule150R_simple_init.ca")
        actual = self._evolve_reversible_ca(expected, 150)
        np.testing.assert_equal(expected, actual)

    def test_rule150R_simple_init_parallel(self):
        expected = self._convert_to_matrix("rule150R_simple_init.ca")
        actual = self._evolve_reversible_ca_parallel(expected, 150)
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_reversible_ca(expected, rule_number):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacencies = adjacency.cellular_automaton(n=size, r=1)
        r = ReversibleRule(lambda n, c, t: rules.nks_ca_rule(n, c, rule_number))
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=rows,
                                            activity_rule=r.activity_rule, past_conditions=[initial_conditions])
        return activities

    @staticmethod
    def _evolve_reversible_ca_parallel(expected, rule_number):
        rows, size = expected.shape
        initial_conditions = np.array(expected[0]).flatten()
        adjacencies = adjacency.cellular_automaton(n=size, r=1)
        r = ReversibleRule(lambda n, c, t: rules.nks_ca_rule(n, c, rule_number))
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=rows,
                                            activity_rule=r.activity_rule, past_conditions=[initial_conditions],
                                            parallel=True, processes=2)
        return activities
