import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt

"""
This is essentially the Erdős–Rényi model. We begin with a set of unconnected nodes, and randomly pick nodes to connect
at each timestep. The degree distribution for such a network is P(k)=2^-k, where k is the node degree.
"""

if __name__ == "__main__":

    N = 200
    network = ntm.topology.disconnected(N)

    def topology_rule(ctx):
        choices = [int(i) for i in np.random.choice([n for n in ctx.network.nodes], size=2, replace=True)]
        ctx.network.add_edge(choices[1], choices[0])
        ctx.network.add_edge(choices[0], choices[1])

        return ctx.network

    trajectory = ntm.evolve(initial_conditions=[1]*N, network=network,
                            topology_rule=topology_rule, timesteps=N)

    # plot degree distribution
    degree_counts = {}
    last_network = trajectory[-1].network
    for node in last_network.nodes:
        # because links are bidirectional, we can simply count the outgoing links
        # subtract 1 to adjust for the self-link
        degree = last_network.out_degree(node) - 1
        if degree not in degree_counts:
            degree_counts[degree] = 0
        degree_counts[degree] += 1

    x = [i for i in range(1, max(degree_counts) + 1)]
    height = [degree_counts[i] if i in degree_counts else 0 for i in x]

    y = [2**-k for k in x]

    plt.bar(x, height)
    plt.xlabel("Node degree")
    plt.ylabel("Frequency")
    plt.twinx()
    plt.plot(x, y, color="r")
    plt.ylabel("Probability")
    plt.text(0.51, 0.76, "$p_{k} = 2^{-k}$", transform=plt.gca().transAxes, color="r")
    plt.show()

    # NOTE: node self-links are not rendered
    ntm.animate_network(trajectory, interval=350, with_labels=False)
