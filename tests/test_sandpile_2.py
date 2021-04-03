import netomaton as ntm
from .rule_test import *


class TestSandpile(RuleTest):

    def test_sandpile(self):
        np.random.seed(0)
        sandpile = ntm.Sandpile_2(rows=60, cols=60)

        initial_conditions = np.random.randint(5, size=3600)

        def perturb(pctx):
            # drop a grain on some node at the 85th timestep
            if pctx.timestep == 85 and pctx.node_label == 1034:
                return pctx.node_activity + 1
            return pctx.node_activity

        activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=sandpile.adjacency_matrix,
                                     activity_rule=sandpile.activity_rule, perturbation=perturb,
                                     timesteps=110)

        expected = self._convert_to_list_of_lists("sandpile.ca")
        np.testing.assert_equal(expected, activities)
