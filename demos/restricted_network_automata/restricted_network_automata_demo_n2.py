import networkx as nx
import netomaton as ntm


if __name__ == '__main__':
    """
    In Smith's Restricted NA Game of Life example, they define an Underlying network that restricts what links can be 
    formed. Alternatively, one can instead begin with a lattice network, and change the link weights; or, one can add 
    additional links between the already connected nodes.

    Nevertheless, here, the Restricted NA Game of Life example is implemented using an underlying lattice, as 
    described in the paper: Smith, David MD, et al. "Network automata: Coupling structure and function in 
    dynamic networks." Advances in Complex Systems 14.03 (2011): 317-339. 
    Figure 1.
    """

    underlying_network = ntm.topology.lattice(dim=(1, 6, 6), periodic=True)
    initial_network = ntm.Network(n=36)

    # spaceship
    initial_network.add_edge(9, 10)
    initial_network.add_edge(10, 9)
    initial_network.add_edge(3, 9)
    initial_network.add_edge(9, 3)
    initial_network.add_edge(15, 9)
    initial_network.add_edge(9, 15)
    initial_network.add_edge(15, 14)
    initial_network.add_edge(14, 15)
    initial_network.add_edge(8, 14)
    initial_network.add_edge(14, 8)
    initial_network.add_edge(2, 8)
    initial_network.add_edge(8, 2)
    initial_network.add_edge(7, 8)
    initial_network.add_edge(8, 7)

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
                if combined_in_degrees == 2 and not curr_network.has_edge(j, i) and underlying_network.has_edge(j, i):
                    new_network.add_edge(j, i)
                # a link will survive if the combined degree of the two nodes it connects is 3
                elif combined_in_degrees == 3 and curr_network.has_edge(j, i):
                    pass
                # a link dies if it exists
                elif curr_network.has_edge(j, i):
                    new_network.remove_edge(j, i)
        return new_network

    trajectory = ntm.evolve_n2(network=initial_network, topology_rule=topology_rule, timesteps=6)

    pos = nx.spring_layout(ntm.topology.lattice(dim=(1, 6, 6), periodic=False).to_networkx())
    ntm.animate_network_n2(trajectory, layout=pos, interval=500)
