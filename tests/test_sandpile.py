import netomaton as ntm
from .rule_test import *


class TestSandpile(RuleTest):

    def test_sandpile(self):
        np.random.seed(0)
        sandpile = ntm.Sandpile(rows=60, cols=60)

        initial_conditions = np.random.randint(5, size=3600)

        def perturb(pctx):
            # drop a grain on some node at the 85th timestep
            if pctx.timestep == 85 and pctx.node_index == 1034:
                return pctx.node_activity + 1
            return pctx.node_activity

        activities, _ = ntm.evolve(initial_conditions, sandpile.adjacency_matrix, timesteps=110,
                                   activity_rule=sandpile.activity_rule, perturbation=perturb, parallel=True)

        expected = self._convert_to_list_of_lists("sandpile.ca")
        np.testing.assert_equal(expected, activities.tolist())
