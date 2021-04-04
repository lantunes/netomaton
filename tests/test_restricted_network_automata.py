import netomaton as ntm
from .rule_test import *


class TestRestrictedNetworkAutomata(RuleTest):

    def test_rna_gol(self):
        underlying_network = ntm.topology.adjacency.lattice(dim=(1, 6, 6), periodic=True)
        initial_network = ntm.topology.table.disconnected(36)

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

        def connectivity_rule(cctx):
            curr_map = cctx.connectivity_map
            new_map = ntm.copy_connectivity_map(curr_map)
            for i in range(len(underlying_network)):
                in_degree_i = sum([len(c) for c in curr_map[i].values()])
                for j in range(len(underlying_network)):
                    if i == j: continue
                    in_degree_j = sum([len(c) for c in curr_map[j].values()])
                    combined_in_degrees = in_degree_i + in_degree_j
                    # a non-existent link will be “born” if the combined degrees of the
                    #   two nodes between which it might exist is 2
                    if combined_in_degrees == 2 and j not in curr_map[i] and underlying_network[i][j] == 1:
                        new_map[i][j] = [{}]
                    # a link will survive if the combined degree of the two nodes it connects is 3
                    elif combined_in_degrees == 3 and j in curr_map[i]:
                        pass
                    # a link dies if it exists
                    else:
                        if j in curr_map[i]: del new_map[i][j]
            return new_map

        _, connectivities = ntm.evolve(topology=initial_network, connectivity_rule=connectivity_rule, timesteps=6)

        expected = self._convert_from_literal("restricted_network_automata.txt")
        self.assertEqual(expected, connectivities)
