import netomaton.network as AdjacencyMatrix
import netomaton.rules as ActivityRule
from netomaton import AsynchronousRule, evolve
from .rule_test import *


class TestAsynchronousRule(RuleTest):

    def test_sequential_left_to_right(self):
        expected = self._convert_to_matrix("rule60_sequential_simple_init.ca")
        adjacencies = AdjacencyMatrix.cellular_automaton(n=21)
        initial_conditions = [0]*10 + [1] + [0]*10
        r = AsynchronousRule(activity_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 60), update_order=range(1, 20))
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=19*20,
                                            activity_rule=r.activity_rule)
        np.testing.assert_equal(expected, activities[::19])

    def test_sequential_random(self):
        expected = self._convert_to_matrix("rule90_sequential_simple_init.ca")
        adjacencies = AdjacencyMatrix.cellular_automaton(n=21)
        initial_conditions = [0]*10 + [1] + [0]*10
        update_order = [19, 11, 4, 9, 6, 16, 10, 2, 17, 1, 12, 15, 5, 3, 8, 18, 7, 13, 14]
        r = AsynchronousRule(activity_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 90), update_order=update_order)
        activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=19*20,
                                            activity_rule=r.activity_rule)
        np.testing.assert_equal(expected, activities[::19])
