import netomaton as ntm
from .rule_test import *


class TestLangtonsLoop(RuleTest):

    def test_langtons_loop(self):
        dim = (75, 75)
        rule = ntm.LangtonsLoop(dim=dim)

        initial_conditions = rule.init_loops(1, [40], [25])

        trajectory = ntm.evolve(initial_conditions=initial_conditions,
                                network=rule.network, timesteps=150,
                                activity_rule=rule.activity_rule)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("langtons_loop.ca")

        np.testing.assert_equal(expected, activities_list)

    def test_langtons_loop_memoized(self):
        dim = (75, 75)
        rule = ntm.LangtonsLoop(dim=dim)

        initial_conditions = rule.init_loops(1, [40], [25])

        trajectory = ntm.evolve(initial_conditions=initial_conditions,
                                network=rule.network, timesteps=150,
                                activity_rule=rule.activity_rule, memoize=True)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("langtons_loop.ca")

        np.testing.assert_equal(expected, activities_list)
