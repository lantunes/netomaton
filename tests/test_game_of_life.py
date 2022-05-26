import netomaton as ntm
from .rule_test import *


class TestGameOfLifeRule(RuleTest):

    def test_gol(self):
        network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')
        expected = self._convert_to_list_of_lists("game_of_life.ca")

        initial_conditions = ntm.init_simple2d(60, 60)

        # Light Weight Space Ship (LWSS)
        initial_conditions[1125] = 1
        initial_conditions[1128] = 1
        initial_conditions[1184] = 1
        initial_conditions[1244] = 1
        initial_conditions[1248] = 1
        initial_conditions[1304] = 1
        initial_conditions[1305] = 1
        initial_conditions[1306] = 1
        initial_conditions[1307] = 1

        # Glider
        initial_conditions[1710] = 1
        initial_conditions[1771] = 1
        initial_conditions[1829] = 1
        initial_conditions[1830] = 1
        initial_conditions[1831] = 1

        # Blinker
        initial_conditions[2415] = 1
        initial_conditions[2416] = 1
        initial_conditions[2417] = 1

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=180,
                                activity_rule=ntm.rules.game_of_life_rule)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        np.testing.assert_equal(expected, activities)
