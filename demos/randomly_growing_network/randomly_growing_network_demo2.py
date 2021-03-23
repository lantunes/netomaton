import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt
import random

"""
A minimal model of a growing network. 
"At each time step, a new vertex is added; then, with probability δ, two vertices are chosen uniformly at random and 
joined by an undirected edge. This process is repeated for t time steps."

If the probability of attaching two node is p, then the probability of a randomly
chosen node have degree k is: (2p)^k / (1 + 2p)^(k+1).

See: "Are randomly grown graphs really random?", https://arxiv.org/abs/cond-mat/0104546

Callaway, D. S., Hopcroft, J. E., Kleinberg, J. M., Newman, M. E., & Strogatz, S. H. (2001). 
Are randomly grown graphs really random?. Physical Review E, 64(4), 041902.
 
"""

if __name__ == "__main__":

    # probability of attaching two nodes
    delta = 1.0

    adjacency_matrix = [[1.0]]  # begin with a single-node network

    def connectivity_rule(cctx):
        num_nodes = len(cctx.connectivity_map)
        new_label = num_nodes
        cctx.connectivity_map[new_label] = {new_label: [{}]}
        if random.random() < delta:
            # choose 2 nodes at random, without replacement
            choices = np.random.choice(list(cctx.connectivity_map.keys()), size=2, replace=False)
            cctx.connectivity_map[choices[0]][choices[1]] = [{}]
            cctx.connectivity_map[choices[1]][choices[0]] = [{}]

        return cctx.connectivity_map

    _, connectivities = ntm.evolve_2(initial_conditions=[1], topology=adjacency_matrix,
                                     connectivity_rule=connectivity_rule, timesteps=200)

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

    y = [((2*delta)**k)/((1 + 2*delta)**(k+1)) for k in x]

    plt.bar(x, height)
    plt.xlabel("Node degree")
    plt.ylabel("Frequency")
    plt.twinx()
    plt.plot(x, y, color="r")
    plt.ylabel("Probability")
    plt.text(0.51, 0.76, "$p_k = \\frac{(2\\delta)^k}{(1 + 2\\delta)^{k+1}}$", transform=plt.gca().transAxes, color="r")
    plt.show()

    # animate time evolution of the network (NOTE: node self-links are not rendered)
    ntm.animate_network(connectivities, interval=350, layout="spring", with_labels=False)
