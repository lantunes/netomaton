from netomaton.topology import adjacency
import netomaton.rules as rules
from netomaton import AsynchronousRule, evolve
from .rule_test import *


class TestAsynchronousRule(RuleTest):

    def test_sequential_left_to_right(self):
        expected = self._convert_to_matrix("rule60_sequential_simple_init.ca")
        adjacency_matrix = adjacency.cellular_automaton(n=21)
        initial_conditions = [0]*10 + [1] + [0]*10
        r = AsynchronousRule(activity_rule=rules.nks_ca_rule(60), update_order=range(1, 20))
        activities, adjacencies = evolve(initial_conditions, adjacency_matrix, timesteps=19*20,
                                         activity_rule=r)
        np.testing.assert_equal(expected, activities[::19])

    def test_sequential_random(self):
        expected = self._convert_to_matrix("rule90_sequential_simple_init.ca")
        adjacency_matrix = adjacency.cellular_automaton(n=21)
        initial_conditions = [0]*10 + [1] + [0]*10
        update_order = [19, 11, 4, 9, 6, 16, 10, 2, 17, 1, 12, 15, 5, 3, 8, 18, 7, 13, 14]
        r = AsynchronousRule(activity_rule=rules.nks_ca_rule(90), update_order=update_order)
        activities, adjacencies = evolve(initial_conditions, adjacency_matrix, timesteps=19*20,
                                         activity_rule=r)
        np.testing.assert_equal(expected, activities[::19])
