import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt
import random

"""
A minimal model of a growing network. 
"At each time step, a new vertex is added; then, with probability δ, two vertices are chosen uniformly at random and 
joined by an undirected edge. This process is repeated for t time steps."

If the probability of attaching two nodes is p, then the probability of a randomly
chosen node have degree k is: (2p)^k / (1 + 2p)^(k+1).

See: "Are randomly grown graphs really random?", https://arxiv.org/abs/cond-mat/0104546

Callaway, D. S., Hopcroft, J. E., Kleinberg, J. M., Newman, M. E., & Strogatz, S. H. (2001). 
Are randomly grown graphs really random?. Physical Review E, 64(4), 041902.
 
"""

if __name__ == "__main__":

    # probability of attaching two nodes
    delta = 1.0

    network = ntm.topology.disconnected(1)  # begin with a single-node network

    def topology_rule(ctx):
        num_nodes = len(ctx.network.nodes)
        new_label = num_nodes
        ctx.network.add_node(new_label)
        if random.random() < delta:
            # choose 2 nodes at random, without replacement
            choices = [int(i) for i in np.random.choice(list(ctx.network.nodes), size=2, replace=False)]
            ctx.network.add_edge(choices[1], choices[0])
            ctx.network.add_edge(choices[0], choices[1])

        return ctx.network

    trajectory = ntm.evolve(network=network, topology_rule=topology_rule, timesteps=200)

    # plot degree distribution
    ntm.plot_degree_distribution(trajectory[-1].network, out_degree=True,
                                 equation=lambda k: ((2*delta)**k)/((1 + 2*delta)**(k+1)),
                                 equation_text="$p_k = \\frac{(2\\delta)^k}{(1 + 2\\delta)^{k+1}}$")

    # animate time evolution of the network (NOTE: node self-links are not rendered)
    ntm.animate_network(trajectory, interval=350, layout="spring", with_labels=False)
