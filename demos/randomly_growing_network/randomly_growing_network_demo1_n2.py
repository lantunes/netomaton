import netomaton as ntm
import numpy as np

"""
A growing version of the Erdős–Rényi model. We begin with a single unconnected node, and add a new node at each 
timestep, attaching it randomly to a node in the network. Nodes added earlier in the evolution have a greater 
probability of having a larger degree.

See: Jackson, M. O. (2010). Social and economic networks. Princeton university press. Chapter 5, "Growing Random Networks" 
"""

if __name__ == "__main__":

    network = ntm.Network()
    network.add_node(0)

    def topology_rule(ctx):
        num_nodes = len(ctx.network.nodes)
        new_label = num_nodes
        ctx.network.add_node(new_label)
        connect_to = int(np.random.choice(list(range(num_nodes))))
        ctx.network.add_edge(new_label, connect_to)

        return ctx.network

    trajectory = ntm.evolve_n2(initial_conditions=[1], network=network,
                               topology_rule=topology_rule, timesteps=200)

    # animate time evolution of the network (NOTE: node self-links are not rendered)
    ntm.animate_network_n2(trajectory, interval=350, layout="spring", with_labels=False)
