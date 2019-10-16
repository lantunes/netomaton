import netomaton as ntm
from .rule_test import *


class TestRandomlyGrowingNetwork(RuleTest):

    def test_model(self):
        np.random.seed(0)
        expected = self._convert_to_list_of_list_of_lists("randomly_growing_network.ca")

        adjacency_matrix = [[1]]  # begin with a single-node network

        def activity_rule(ctx):
            # TODO this is a hack to get the activity list and adjacency matrix in sync
            curr_idx = ctx.node_index
            if ctx.timestep == curr_idx + 1:
                ctx.insert(curr_idx, 1)
            # we aren't interested in the activity in this example, so the node's activity will always be the same
            return 1

        def connectivity_rule(cctx):
            new_adjacencies = [[i for i in x] for x in cctx.last_adjacencies]

            for row in new_adjacencies:
                row.append(0)
            new_adjacencies.append([0 for _ in range(len(new_adjacencies) + 1)])

            new_idx = len(new_adjacencies) - 1
            connect_to = np.random.choice(list(range(len(new_adjacencies))))
            new_adjacencies[connect_to][new_idx] = 1
            new_adjacencies[new_idx][connect_to] = 1

            return new_adjacencies

        _, adjacencies = ntm.evolve(initial_conditions=[1], adjacency_matrix=adjacency_matrix,
                                    activity_rule=activity_rule, connectivity_rule=connectivity_rule, timesteps=25)

        np.testing.assert_equal(expected, adjacencies)
