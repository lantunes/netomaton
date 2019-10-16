import netomaton as ntm
from .rule_test import *


class TestRandomAttachmentModel(RuleTest):

    def test_model(self):
        np.random.seed(0)
        expected = self._convert_to_matrix2d("random_attachment_model.ca")

        # begin with a fully disconnected network of size N
        N = 25
        adjacency_matrix = [[0 for _ in range(N)] for _ in range(N)]

        def activity_rule(ctx):
            return 1

        def connectivity_rule(cctx):
            new_adjacencies = [[i for i in x] for x in cctx.last_adjacencies]

            idx1 = np.random.choice(list(range(len(new_adjacencies))))
            idx2 = np.random.choice(list(range(len(new_adjacencies))))

            new_adjacencies[idx1][idx2] = 1
            new_adjacencies[idx2][idx1] = 1

            return new_adjacencies

        _, adjacencies = ntm.evolve(initial_conditions=[1] * N, adjacency_matrix=adjacency_matrix,
                                    activity_rule=activity_rule, connectivity_rule=connectivity_rule, timesteps=N)

        np.testing.assert_equal(expected, adjacencies)
