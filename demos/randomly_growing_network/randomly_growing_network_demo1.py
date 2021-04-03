import netomaton as ntm
import numpy as np

"""
A growing version of the Erdős–Rényi model. We begin with a single unconnected node, and add a new node at each 
timestep, attaching it randomly to a node in the network. Nodes added earlier in the evolution have a greater 
probability of having a larger degree.

See: Jackson, M. O. (2010). Social and economic networks. Princeton university press. Chapter 5, "Growing Random Networks" 
"""

if __name__ == "__main__":

    adjacency_matrix = [[1.0]]  # begin with a single-node network

    def connectivity_rule(cctx):
        num_nodes = len(cctx.connectivity_map)
        new_label = num_nodes
        cctx.connectivity_map[new_label] = {}
        connect_to = np.random.choice(list(range(num_nodes)))
        cctx.connectivity_map[connect_to][new_label] = [{}]
        cctx.connectivity_map[new_label][connect_to] = [{}]

        return cctx.connectivity_map

    _, connectivities = ntm.evolve(initial_conditions=[1], topology=adjacency_matrix,
                                   connectivity_rule=connectivity_rule, timesteps=200)

    # animate time evolution of the network (NOTE: node self-links are not rendered)
    ntm.animate_network(connectivities, interval=350, layout="spring", with_labels=False)
