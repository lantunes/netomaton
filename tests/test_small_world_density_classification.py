import numpy as np

import netomaton as ntm
from .rule_test import *


class TestSmallWorldDensityClassification(RuleTest):

    def test_small_world_density_classification(self):
        np.random.seed(0)

        network = ntm.topology.watts_strogatz_graph(n=149, k=8, p=0.5, seed=0)

        initial_conditions = np.random.randint(0, 2, 149)

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                                activity_rule=ntm.rules.majority_rule, timesteps=149)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = self._convert_to_list_of_lists("small_world_density_classification.ca")
        np.testing.assert_equal(expected, activities)
