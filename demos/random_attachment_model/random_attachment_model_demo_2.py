import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt

"""
This is essentially the Erdős–Rényi model. We begin with a set of unconnected nodes, and randomly pick nodes to connect
at each timestep. The degree distribution for such a network is P(k)=2^-k, where k is the node degree.
"""

if __name__ == "__main__":

    N = 200
    adjacency_matrix = [[0 for _ in range(N)] for _ in range(N)]  # begin with a fully disconnected network of size N

    def activity_rule(ctx):
        # we aren't interested in the activity in this example, so the node's activity will always be the same
        return 1

    def connectivity_rule(cctx):
        choices = np.random.choice([n for n in cctx.connectivities], size=2, replace=False)
        cctx.connectivities[choices[0]][choices[1]] = 1.0
        cctx.connectivities[choices[1]][choices[0]] = 1.0

        return cctx.connectivities

    _, connectivities = ntm.evolve_2(initial_conditions=[1]*N, topology=adjacency_matrix,
                                     activity_rule=activity_rule, connectivity_rule=connectivity_rule, timesteps=N)

    # plot degree distribution
    degree_counts = {}
    for row in connectivities[-1]:
        # because links are bidirectional, we can simply count the outgoing links
        # subtract 1 to adjust for the self-link
        degree = np.count_nonzero(row) - 1
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
    ntm.animate_network(connectivities, interval=350, with_labels=False)
