import netomaton as ntm
from .rule_test import *


class TestRandomlyGrowingNetwork(RuleTest):

    def test_model(self):
        np.random.seed(0)
        expected = self._convert_to_list_of_list_of_lists("randomly_growing_network.ca")

        network = ntm.topology.from_adjacency_matrix([[1]])  # begin with a single-node network

        def topology_rule(ctx):
            num_nodes = len(ctx.network.nodes)
            new_label = num_nodes
            ctx.network.add_node(new_label)
            connect_to = int(np.random.choice(list(range(num_nodes))))
            ctx.network.add_edge(new_label, connect_to)
            ctx.network.add_edge(connect_to, new_label)

            return ctx.network

        trajectory = ntm.evolve(initial_conditions=[1], network=network,
                                topology_rule=topology_rule, timesteps=25)

        topology = [state.network.to_adjacency_matrix() for state in trajectory]
        np.testing.assert_equal(expected, topology)
