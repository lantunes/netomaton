import numpy as np

import netomaton as ntm
from .rule_test import *


class TestLogisticMap(RuleTest):

    def test_logistic_map(self):
        a = 2.5
        timesteps = 20

        adjacency_matrix = [[1]]
        initial_conditions = [0.5]

        def activity_rule(ctx):
            return a * ctx.current_activity * (1 - ctx.current_activity)

        activities, _ = ntm.evolve(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                   activity_rule=activity_rule, timesteps=timesteps)

        expected = [[0.5], [0.625], [0.5859375], [0.606536865234375], [0.5966247408650815], [0.6016591486318896],
                    [0.5991635437485985], [0.6004164789780495], [0.5997913268741273], [0.6001042277017528],
                    [0.599947858990589], [0.6000260637079934], [0.5999869664477111], [0.6000065163514607],
                    [0.5999967417181126], [0.6000016291144027], [0.5999991854361636], [0.6000004072802594],
                    [0.5999997963594557], [0.6000001018201685]]

        np.testing.assert_equal(expected, activities)
