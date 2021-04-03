import netomaton as ntm
from .rule_test import *


class TestHexEvolution(RuleTest):

    def test_snowflake(self):
        adjacency_matrix = ntm.topology.adjacency.cellular_automaton2d(60, 60, r=1, neighbourhood="Hex")

        initial_conditions = ntm.init_simple2d(60, 60)

        def activity_rule(ctx):
            return 1 if sum(ctx.neighbourhood_activities) == 1 else ctx.current_activity

        activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=31,
                                     activity_rule=activity_rule)

        expected = self._convert_to_list_of_lists("snowflake.ca")
        np.testing.assert_equal(expected, activities)
