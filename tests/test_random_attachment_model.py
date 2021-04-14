import netomaton as ntm
from .rule_test import *


class TestRandomAttachmentModel(RuleTest):

    def test_model(self):
        np.random.seed(0)
        expected = self._convert_to_matrix2d("random_attachment_model.ca")

        # begin with a fully disconnected network of size N
        N = 25
        adjacency_matrix = [[0 for _ in range(N)] for _ in range(N)]

        def connectivity_rule(cctx):
            choices = [int(i) for i in np.random.choice([n for n in cctx.connectivity_map], size=2, replace=True)]
            cctx.connectivity_map[choices[0]][choices[1]] = [{}]
            cctx.connectivity_map[choices[1]][choices[0]] = [{}]

            return cctx.connectivity_map

        _, connectivities = ntm.evolve(initial_conditions=[1] * N, topology=adjacency_matrix,
                                       connectivity_rule=connectivity_rule, timesteps=N)

        np.testing.assert_equal(expected, connectivities)
