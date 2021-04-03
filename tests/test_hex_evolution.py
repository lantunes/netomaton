import netomaton as ntm
from .rule_test import *


class TestHexEvolution(RuleTest):

    def test_snowflake(self):
        adjacency_matrix = ntm.topology.adjacency.cellular_automaton2d(60, 60, r=1, neighbourhood="Hex")

        initial_conditions = ntm.init_simple2d(60, 60)

        activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=31,
                                   activity_rule=lambda ctx: 1 if sum(ctx.activities) == 1 else ctx.current_activity)

        expected = self._convert_to_list_of_lists("snowflake.ca")
        np.testing.assert_equal(expected, activities.tolist())
