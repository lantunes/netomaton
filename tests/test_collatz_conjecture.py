import netomaton as ntm
from .rule_test import *


class TestCollatzConjecture(RuleTest):

    def test_collatz_conjecture(self):

        network = ntm.topology.from_adjacency_matrix([[1]])

        def activity_rule(ctx):
            n = ctx.current_activity
            if n % 2 == 0:
                # number is even
                return n / 2
            else:
                return 3 * n + 1

        def input(t, activities, n):
            if activities[0] == 1:
                return None
            return 1

        initial_conditions = [3]

        trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions,
                                activity_rule=activity_rule, input=input)

        activities = ntm.get_activities_over_time_as_list(trajectory)

        self.assertEqual([[3], [10], [5.0], [16.0], [8.0], [4.0], [2.0], [1.0]], activities)
