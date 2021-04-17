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

        model = ntm.FungalGrowthModel_N2(R_E, width, height, initial_conditions, seed=20210408, verbose=False)

        trajectory = ntm.evolve_n2(network=model.network, initial_conditions=initial_conditions,
                                   activity_rule=model.activity_rule, topology_rule=model.topology_rule,
                                   update_order=model.update_order, timesteps=timesteps)

        activities_list = [list(n.activities.values()) for n in trajectory.values()]
        expected = self._convert_to_list_of_lists("fungal_growth.ca", dtype=float)

        np.testing.assert_almost_equal(expected, activities_list, decimal=11)

        expected = self._convert_from_literal("fungal_growth_model_n2.txt")

        actual = {i: s.network.to_dict() for i, s in trajectory.items()}
        self.assertEqual(expected, actual)

    def test_fungal_growth_with_resource_layer(self):
        R_E = 80000.0
        timesteps = 10
        width = 10
        height = 10
        initial_conditions = ntm.init_simple2d(width, height, val=R_E, dtype=float)
        resource_layer = [0 for i in range(width * height)]
        for nz in np.nonzero(initial_conditions)[0]:
            resource_layer[nz] = 1

        model = ntm.FungalGrowthModel_N2(R_E, width, height, initial_conditions, resource_layer=resource_layer,
                                         seed=20210408, verbose=False)

        trajectory = ntm.evolve_n2(network=model.network, initial_conditions=initial_conditions,
                                   activity_rule=model.activity_rule, topology_rule=model.topology_rule,
                                   update_order=model.update_order, timesteps=timesteps)

        activities_list = [list(n.activities.values()) for n in trajectory.values()]
        expected = self._convert_to_list_of_lists("fungal_growth.ca", dtype=float)

        np.testing.assert_almost_equal(expected, activities_list, decimal=11)

        expected = self._convert_from_literal("fungal_growth_model_n2.txt")

        actual = {i: s.network.to_dict() for i, s in trajectory.items()}
        self.assertEqual(expected, actual)
