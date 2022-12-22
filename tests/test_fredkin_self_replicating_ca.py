import netomaton as ntm
from .rule_test import *


class TestFredkinSelfReplicatingCA(RuleTest):

    def test_von_neumann(self):
        network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood="von Neumann")

        initial_conditions = ntm.init_simple2d(60, 60)
        # the letter "E"
        initial_conditions[1709] = 1
        initial_conditions[1710] = 1
        initial_conditions[1711] = 1
        initial_conditions[1769] = 1
        initial_conditions[1829] = 1
        initial_conditions[1830] = 1
        initial_conditions[1831] = 1
        initial_conditions[1889] = 1
        initial_conditions[1949] = 1
        initial_conditions[1950] = 1
        initial_conditions[1951] = 1

        def activity_rule(ctx):
            return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 2

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=20,
                                activity_rule=activity_rule)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("fredkin_self_replicating_ca_vonneumann.ca")

        np.testing.assert_equal(expected, activities_list)

    def test_von_neumann_memoized(self):
        network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood="von Neumann")

        initial_conditions = ntm.init_simple2d(60, 60)
        # the letter "E"
        initial_conditions[1709] = 1
        initial_conditions[1710] = 1
        initial_conditions[1711] = 1
        initial_conditions[1769] = 1
        initial_conditions[1829] = 1
        initial_conditions[1830] = 1
        initial_conditions[1831] = 1
        initial_conditions[1889] = 1
        initial_conditions[1949] = 1
        initial_conditions[1950] = 1
        initial_conditions[1951] = 1

        def activity_rule(ctx):
            return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 2

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=20,
                                activity_rule=activity_rule, memoize=True)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("fredkin_self_replicating_ca_vonneumann.ca")

        np.testing.assert_equal(expected, activities_list)

    def test_moore(self):
        network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood="Moore")

        initial_conditions = ntm.init_simple2d(60, 60)
        # the letter "E"
        initial_conditions[1709] = 1
        initial_conditions[1710] = 1
        initial_conditions[1711] = 1
        initial_conditions[1769] = 1
        initial_conditions[1829] = 1
        initial_conditions[1830] = 1
        initial_conditions[1831] = 1
        initial_conditions[1889] = 1
        initial_conditions[1949] = 1
        initial_conditions[1950] = 1
        initial_conditions[1951] = 1

        def activity_rule(ctx):
            return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 2

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=20,
                                activity_rule=activity_rule)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("fredkin_self_replicating_ca_moore.ca")

        np.testing.assert_equal(expected, activities_list)

    def test_moore_memoized(self):
        network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood="Moore")

        initial_conditions = ntm.init_simple2d(60, 60)
        # the letter "E"
        initial_conditions[1709] = 1
        initial_conditions[1710] = 1
        initial_conditions[1711] = 1
        initial_conditions[1769] = 1
        initial_conditions[1829] = 1
        initial_conditions[1830] = 1
        initial_conditions[1831] = 1
        initial_conditions[1889] = 1
        initial_conditions[1949] = 1
        initial_conditions[1950] = 1
        initial_conditions[1951] = 1

        def activity_rule(ctx):
            return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 2

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=20,
                                activity_rule=activity_rule, memoize=True)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("fredkin_self_replicating_ca_moore.ca")

        np.testing.assert_equal(expected, activities_list)

    def test_multicolor(self):
        network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood="von Neumann")

        initial_conditions = ntm.init_simple2d(60, 60)
        # the letter "E"
        initial_conditions[1709] = 0
        initial_conditions[1710] = 1
        initial_conditions[1711] = 2
        initial_conditions[1769] = 3
        initial_conditions[1829] = 4
        initial_conditions[1830] = 5
        initial_conditions[1831] = 6
        initial_conditions[1889] = 7
        initial_conditions[1949] = 8
        initial_conditions[1950] = 9
        initial_conditions[1951] = 10

        def activity_rule(ctx):
            return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 11

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=23,
                                activity_rule=activity_rule)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("fredkin_self_replicating_ca_multicolor.ca")

        np.testing.assert_equal(expected, activities_list)

    def test_multicolor_memoized(self):
        network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood="von Neumann")

        initial_conditions = ntm.init_simple2d(60, 60)
        # the letter "E"
        initial_conditions[1709] = 0
        initial_conditions[1710] = 1
        initial_conditions[1711] = 2
        initial_conditions[1769] = 3
        initial_conditions[1829] = 4
        initial_conditions[1830] = 5
        initial_conditions[1831] = 6
        initial_conditions[1889] = 7
        initial_conditions[1949] = 8
        initial_conditions[1950] = 9
        initial_conditions[1951] = 10

        def activity_rule(ctx):
            return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 11

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=23,
                                activity_rule=activity_rule, memoize=True)

        activities_list = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("fredkin_self_replicating_ca_multicolor.ca")

        np.testing.assert_equal(expected, activities_list)
