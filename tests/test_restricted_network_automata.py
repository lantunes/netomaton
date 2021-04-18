import netomaton as ntm
from .rule_test import *


class TestRestrictedNetworkAutomata(RuleTest):

    def test_rna_gol(self):
        underlying_network = ntm.topology.lattice(dim=(1, 6, 6), periodic=True)
        initial_network = ntm.Network(n=36)

        # spaceship
        initial_network[9][10] = [{}]
        initial_network[10][9] = [{}]
        initial_network[3][9] = [{}]
        initial_network[9][3] = [{}]
        initial_network[15][9] = [{}]
        initial_network[9][15] = [{}]
        initial_network[15][14] = [{}]
        initial_network[14][15] = [{}]
        initial_network[8][14] = [{}]
        initial_network[14][8] = [{}]
        initial_network[2][8] = [{}]
        initial_network[8][2] = [{}]
        initial_network[7][8] = [{}]
        initial_network[8][7] = [{}]

        def topology_rule(ctx):
            curr_network = ctx.network
            new_network = ctx.network.copy()
            for i in underlying_network.nodes:
                in_degree_i = curr_network.in_degree(i)
                for j in underlying_network.nodes:
                    if i == j:
                        continue
                    in_degree_j = curr_network.in_degree(j)
                    combined_in_degrees = in_degree_i + in_degree_j
                    # a non-existent link will be “born” if the combined degrees of the
                    #   two nodes between which it might exist is 2
                    if combined_in_degrees == 2 and not curr_network.has_edge(j, i) and underlying_network.has_edge(j,
                                                                                                                    i):
                        new_network.add_edge(j, i)
                    # a link will survive if the combined degree of the two nodes it connects is 3
                    elif combined_in_degrees == 3 and curr_network.has_edge(j, i):
                        pass
                    # a link dies if it exists
                    elif curr_network.has_edge(j, i):
                        new_network.remove_edge(j, i)
            return new_network

        trajectory = ntm.evolve(network=initial_network, topology_rule=topology_rule, timesteps=6)

        topology = [state.network.to_dict() for state in trajectory]
        expected = self._convert_from_literal("restricted_network_automata.txt")
        self.assertEqual(expected, topology)
