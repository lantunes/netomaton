import netomaton as ntm
from .rule_test import *


class TestRandomlyGrowingNetwork(RuleTest):

    def test_model(self):
        np.random.seed(0)
        expected = self._convert_to_list_of_list_of_lists("randomly_growing_network.ca")

        adjacency_matrix = [[1]]  # begin with a single-node network

        def connectivity_rule(cctx):
            num_nodes = len(cctx.connectivity_map)
            new_label = num_nodes
            cctx.connectivity_map[new_label] = {}
            connect_to = int(np.random.choice(list(range(num_nodes))))
            cctx.connectivity_map[connect_to][new_label] = [{}]
            cctx.connectivity_map[new_label][connect_to] = [{}]

            return cctx.connectivity_map

        _, connectivities = ntm.evolve(initial_conditions=[1], topology=adjacency_matrix,
                                       connectivity_rule=connectivity_rule, timesteps=25)

        np.testing.assert_equal(expected, connectivities)
