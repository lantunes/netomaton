import netomaton as ntm
from .rule_test import *


class TestFungalGrowthModel(RuleTest):

    def test_fungal_growth(self):

        R_E = 80000
        timesteps = 10
        width = 10
        height = 10
        initial_conditions = ntm.init_simple2d(width, height, val=R_E)

        model = ntm.FungalGrowthModel(R_E, width, height, initial_conditions, seed=20210408, verbose=False)

        activities, _ = ntm.evolve(topology=model.topology, initial_conditions=initial_conditions,
                                   activity_rule=model.activity_rule, connectivity_rule=model.connectivity_rule,
                                   update_order=model.update_order, timesteps=timesteps)

        activities_list = ntm.convert_activities_map_to_list(activities)
        expected = self._convert_to_list_of_lists("fungal_growth.ca", dtype=float)

        self.assertEqual(expected, activities_list)
