import networkx as nx
import netomaton as ntm


if __name__ == '__main__':
    """
    A significant difference between the Netomaton framework and the NA described by Smith is that in Netomaton the 
    network links can have state (e.g. weights). In Smith's Restricted NA Game of Life example, they define an 
    Underlying network that restricts what links can be formed. Alternatively, one can instead begin with a lattice 
    network, and change the link weights; or, one can add additional links between the already connected nodes.
    
    Nevertheless, here, the Restricted NA Game of Life example is implemented using an underlying lattice, as 
    described in the paper: Smith, David MD, et al. "Network automata: Coupling structure and function in 
    dynamic networks." Advances in Complex Systems 14.03 (2011): 317-339. 
    Figure 1.
    """

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

    G = nx.grid_graph(dim=(1, 6, 6), periodic=False)
    G = nx.convert_node_labels_to_integers(G, first_label=0)
    pos = nx.spring_layout(G)
    ntm.animate_connectivity_map(connectivities, layout=pos, interval=500)
