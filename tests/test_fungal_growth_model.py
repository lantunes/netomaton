import netomaton as ntm
from .rule_test import *
import numpy as np


class TestFungalGrowthModel(RuleTest):

    def test_fungal_growth(self):

        R_E = 80000.0
        timesteps = 10
        width = 10
        height = 10
        initial_conditions = ntm.init_simple2d(width, height, val=R_E, dtype=float)

        model = ntm.FungalGrowthModel(R_E, width, height, initial_conditions, seed=20210408, verbose=False)

        activities, c = ntm.evolve(topology=model.topology, initial_conditions=initial_conditions,
                                   activity_rule=model.activity_rule, connectivity_rule=model.connectivity_rule,
                                   update_order=model.update_order, timesteps=timesteps,
                                   copy_connectivity=model.copy_connectivity)

        activities_list = ntm.convert_activities_map_to_list(activities)
        expected = self._convert_to_list_of_lists("fungal_growth.ca", dtype=float)

        np.testing.assert_almost_equal(expected, activities_list, decimal=11)

        expected = self._convert_from_literal("fungal_growth_model.txt")

        self.assertEqual(expected, c)
