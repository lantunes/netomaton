from netomaton.topology import cellular_automaton
import netomaton.rules as rules
from netomaton import ReversibleRule, evolve, get_activities_over_time_as_list
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
        network = cellular_automaton(n=size, r=1)
        r = ReversibleRule(rules.nks_ca_rule(rule_number))
        trajectory = evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=r, past_conditions=[initial_conditions], timesteps=rows)
        activities = get_activities_over_time_as_list(trajectory)
        return activities
