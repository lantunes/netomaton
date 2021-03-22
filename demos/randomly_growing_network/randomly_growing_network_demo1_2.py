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

    def activity_rule(ctx):
        # we aren't interested in the activity in this example, so the node's activity will always be the same
        return 1.0

    def connectivity_rule(cctx):
        num_nodes = len(cctx.connectivities)
        new_label = num_nodes
        connect_to = np.random.choice(list(range(num_nodes)))
        cctx.connectivities[connect_to][new_label] = 1.0
        cctx.connectivities[new_label] = {new_label: 1.0, connect_to: 1.0}
        cctx.activities[new_label] = 1.0

        return cctx.connectivities

    _, connectivities = ntm.evolve_2(initial_conditions=[1], topology=adjacency_matrix,
                                     activity_rule=activity_rule, connectivity_rule=connectivity_rule, timesteps=200)

    # animate time evolution of the network (NOTE: node self-links are not rendered)
    ntm.animate_network(connectivities, interval=350, layout="spring", with_labels=False)
