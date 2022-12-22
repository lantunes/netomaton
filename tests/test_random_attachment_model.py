import netomaton as ntm
from .rule_test import *


class TestRandomAttachmentModel(RuleTest):

    def test_model(self):
        np.random.seed(0)
        expected = self._convert_to_matrix2d("random_attachment_model.ca")

        # begin with a fully disconnected network of size N
        N = 25
        network = ntm.topology.disconnected(N)

        def topology_rule(ctx):
            choices = [int(i) for i in np.random.choice([n for n in ctx.network.nodes], size=2, replace=True)]
            ctx.network.add_edge(choices[1], choices[0])
            ctx.network.add_edge(choices[0], choices[1])

            return ctx.network

        trajectory = ntm.evolve(initial_conditions=[1] * N, network=network,
                                topology_rule=topology_rule, timesteps=N)

        topology = [state.network.to_adjacency_matrix(sum_multiedges=False) for state in trajectory if state.network]
        np.testing.assert_equal(expected, topology)
