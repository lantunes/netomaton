import collections
import netomaton as ntm
from .rule_test import *


class TestMemoize(RuleTest):

    def test_dependent_unordered(self):
        """
        current node is not in neighbourhood and rule depends on current node;
        For the network
             A
             |
             v
        B -> C <- D
             ^
             |
             E
        define a rule that is totalistic, but that also depends on the current activity of C.
        Note that the network does not include C in the neighbourhood of C.
        """
        network = ntm.Network()
        network.add_edge("A", "C")
        network.add_edge("B", "C")
        network.add_edge("D", "C")
        network.add_edge("E", "C")
        # there is no rotation system specified

        def activity_rule(ctx):
            curr = ctx.current_activity % 10
            neigh = sum(ctx.neighbourhood_activities)
            return curr + neigh

        initial_conditions = {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0}

        trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                                activity_rule=activity_rule, timesteps=12)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = [[0, 1, 0, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0], [0, 1, 6, 1, 0],
                    [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0],
                    [0, 1, 6, 1, 0], [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0]]
        self.assertEqual(activities, expected)

    def test_dependent_unordered_memoized(self):
        """
        current node is not in neighbourhood and rule depends on current node;
        This is an odd situation, since if the current node depends on itself to determine its value at the next
        timestep, then there should be a network connection to itself (and it should be in its neighbourhood). The user
        should provide a custom memoization key for this case.
        For the network
             A
             |
             v
        B -> C <- D
             ^
             |
             E
        define a rule that is totalistic, but that also depends on the current activity of C.
        Note that the network does not include C in the neighbourhood of C.
        """
        network = ntm.Network()
        network.add_edge("A", "C")
        network.add_edge("B", "C")
        network.add_edge("D", "C")
        network.add_edge("E", "C")
        # there is no rotation system specified

        def activity_rule(ctx):
            curr = ctx.current_activity % 10
            neigh = sum(ctx.neighbourhood_activities)
            return curr + neigh

        initial_conditions = {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0}

        trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                                activity_rule=activity_rule, timesteps=12, memoize=True,
                                memoization_key=AbsentDependentUnorderedMemoizationKey())

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = [[0, 1, 0, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0], [0, 1, 6, 1, 0],
                    [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0],
                    [0, 1, 6, 1, 0], [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0]]
        self.assertEqual(activities, expected)

    def test_dependent_ordered(self):
        """
        current node is not in neighbourhood and rule depends on current node;
        For the network
             A
             |
             v
        B -> C <- D
             ^
             |
             E
        define a rule that is totalistic, but that also depends on the current activity of C.
        Note that the network does not include C in the neighbourhood of C.
        """
        network = ntm.Network()
        network.add_edge("A", "C")
        network.add_edge("B", "C")
        network.add_edge("D", "C")
        network.add_edge("E", "C")
        network.rotation_system = {
            "A": (),
            "B": (),
            "C": ("A", "B", "D", "E"),
            "D": (),
            "E": ()
        }

        def activity_rule(ctx):
            curr = ctx.current_activity % 10
            neigh = sum(ctx.neighbourhood_activities)
            return curr + neigh

        initial_conditions = {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0}

        trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                                activity_rule=activity_rule, timesteps=12)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = [[0, 1, 0, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0], [0, 1, 6, 1, 0],
                    [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0],
                    [0, 1, 6, 1, 0], [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0]]
        self.assertEqual(activities, expected)

    def test_dependent_ordered_memoized(self):
        """
        current node is not in neighbourhood and rule depends on current node;
        This is an odd situation, since if the current node depends on itself to determine its value at the next
        timestep, then there should be a network connection to itself (and it should be in its neighbourhood). The user
        should provide a custom memoization key for this case.
        For the network
             A
             |
             v
        B -> C <- D
             ^
             |
             E
        define a rule that is totalistic, but that also depends on the current activity of C.
        Note that the network does not include C in the neighbourhood of C.
        """
        network = ntm.Network()
        network.add_edge("A", "C")
        network.add_edge("B", "C")
        network.add_edge("D", "C")
        network.add_edge("E", "C")
        network.rotation_system = {
            "A": (),
            "B": (),
            "C": ("A", "B", "D", "E"),
            "D": (),
            "E": ()
        }

        def activity_rule(ctx):
            curr = ctx.current_activity % 10
            neigh = sum(ctx.neighbourhood_activities)
            return curr + neigh

        initial_conditions = {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0}

        trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                                activity_rule=activity_rule, timesteps=12, memoize=True,
                                memoization_key=AbsentDependentOrderedMemoizationKey())

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = [[0, 1, 0, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0], [0, 1, 6, 1, 0],
                    [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0], [0, 1, 4, 1, 0],
                    [0, 1, 6, 1, 0], [0, 1, 8, 1, 0], [0, 1, 10, 1, 0], [0, 1, 2, 1, 0]]
        self.assertEqual(activities, expected)

    def test_non_dependent_unordered(self):
        """
        current node is not in neigh. and rule does not depend on current node, neigh. is unordered;
        For the network
             A
             |
             v
        B -> C <- D
             ^
             |
             E
        define a rule that is totalistic, and that doesn't depend on the current activity of C.
        Note that the network does not include C in the neighbourhood of C.
        """
        network = ntm.Network()
        network.add_edge("A", "C")
        network.add_edge("B", "C")
        network.add_edge("D", "C")
        network.add_edge("E", "C")
        # there is no rotation system specified

        def activity_rule(ctx):
            return sum(ctx.neighbourhood_activities) + 1

        initial_conditions = {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0}

        trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                                activity_rule=activity_rule, timesteps=12)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = [[0, 1, 0, 1, 0], [1, 1, 3, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1],
                    [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1],
                    [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1]]
        self.assertEqual(activities, expected)

    def test_non_dependent_unordered_memoized(self):
        """
        current node is not in neigh. and rule does not depend on current node, neigh. is unordered;
        For the network
             A
             |
             v
        B -> C <- D
             ^
             |
             E
        define a rule that is totalistic, and that doesn't depend on the current activity of C.
        Note that the network does not include C in the neighbourhood of C.
        """
        network = ntm.Network()
        network.add_edge("A", "C")
        network.add_edge("B", "C")
        network.add_edge("D", "C")
        network.add_edge("E", "C")
        # there is no rotation system specified

        def activity_rule(ctx):
            return sum(ctx.neighbourhood_activities) + 1

        initial_conditions = {"A": 0, "B": 1, "C": 0, "D": 1, "E": 0}

        trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                                activity_rule=activity_rule, timesteps=12, memoize=True)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = [[0, 1, 0, 1, 0], [1, 1, 3, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1],
                    [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1],
                    [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1], [1, 1, 5, 1, 1]]
        self.assertEqual(activities, expected)



    def test_wireworld_diodes_memoized(self):
        """
        current node is in neigh., and rule depends on current node, but not on order of neigh., e.g. wireworld, GoL;
        in this case, we need a key like (c, {a,b,d,e}), where c is the current node's activity and a, b, d, and e are
        the activities of the neighbouring nodes; essentially, we have to remove the current node's activity from the
        neighbourhood activities when creating the key
        """
        expected = self._convert_to_matrix2d("wireworld_diodes.ca")
        actual = self._evolve_wireworld(expected, memoize=True, memoization_key=WireworldMemoizationKey())
        np.testing.assert_equal(expected, actual)

    def test_wireworld_xor_memoized(self):
        """
        current node is in neigh., and rule depends on current node, but not on order of neigh., e.g. wireworld, GoL;
        in this case, we need a key like (c, {a,b,d,e}), where c is the current node's activity and a, b, d, and e are
        the activities of the neighbouring nodes; essentially, we have to remove the current node's activity from the
        neighbourhood activities when creating the key
        """
        expected = self._convert_to_matrix2d("wireworld_xor.ca")
        actual = self._evolve_wireworld(expected, memoize=True, memoization_key=WireworldMemoizationKey())
        np.testing.assert_equal(expected, actual)

    @staticmethod
    def _evolve_wireworld(expected, memoize=False, memoization_key=None):
        steps, rows, size = expected.shape
        initial_conditions = np.array(expected[0]).reshape(rows * size).flatten()
        network = ntm.topology.cellular_automaton2d(rows=rows, cols=size, neighbourhood="Moore")
        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=steps,
                                activity_rule=ntm.rules.wireworld_rule, memoize=memoize,
                                memoization_key=memoization_key)
        activities = ntm.get_activities_over_time_as_list(trajectory)
        return np.array(activities).reshape((steps, rows, size))


class WireworldMemoizationKey(ntm.MemoizationKey):
    def to_key(self, ctx):
        curr_idx = ctx.neighbour_labels.index(ctx.node_label)
        activities = list(ctx.neighbourhood_activities)
        del activities[curr_idx]
        neigh_key = frozenset(collections.Counter(activities).items())
        return ctx.current_activity, neigh_key


class AbsentDependentOrderedMemoizationKey(ntm.MemoizationKey):
    def to_key(self, ctx):
        return tuple([ctx.current_activity] + ctx.neighbourhood_activities)


class AbsentDependentUnorderedMemoizationKey(ntm.MemoizationKey):
    def to_key(self, ctx):
        return ctx.current_activity, frozenset(collections.Counter(ctx.neighbourhood_activities).items())
