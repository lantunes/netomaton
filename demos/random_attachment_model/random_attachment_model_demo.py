import netomaton as ntm
import numpy as np

"""
This is essentially the Erdős–Rényi model. We begin with a set of unconnected nodes, and randomly pick nodes to connect
at each timestep.

Newman, M. E., Strogatz, S. H., & Watts, D. J. (2001). Random graphs with arbitrary degree distributions and their 
applications. Physical Review E, 64(2), 026118.
"""

if __name__ == "__main__":

    N = 500
    network = ntm.topology.disconnected(N)

    def topology_rule(ctx):
        nodes = [int(i) for i in np.random.choice(list(ctx.network.nodes), size=2, replace=False)]
        if not ctx.network.has_edge(nodes[1], nodes[0]) and not ctx.network.has_edge(nodes[0], nodes[1]):
            ctx.network.add_edge(nodes[1], nodes[0])
            ctx.network.add_edge(nodes[0], nodes[1])

        return ctx.network

    trajectory = ntm.evolve(network=network,
                            topology_rule=topology_rule, timesteps=N)

    # plot degree distribution
    p = 2 / (N - 1)
    ntm.plot_degree_distribution(trajectory[-1].network, out_degree=True,
                                 equation=lambda k: ntm.ncr(N-1, k)*(p**k)*((1-p)**(N-1-k)),
                                 equation_text="$p_{k} = \\binom{N-1}{k} p^k (1-p)^{N-1-k}$")

    ntm.animate_network(trajectory, interval=350, with_labels=False)
