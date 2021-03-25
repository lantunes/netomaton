import netomaton as ntm
import numpy as np

"""
This is essentially the Erdős–Rényi model. We begin with a set of unconnected nodes, and randomly pick nodes to connect
at each timestep. The degree distribution for such a network is P(k)=2^-k, where k is the node degree.
"""

if __name__ == "__main__":

    N = 25
    adjacency_matrix = [[0 for _ in range(N)] for _ in range(N)]  # begin with a fully disconnected network of size N

    def activity_rule(ctx):
        return 1

    def connectivity_rule(cctx):
        new_adjacencies = [[i for i in x] for x in cctx.last_adjacencies]

        idx1 = np.random.choice(list(range(len(new_adjacencies))))
        idx2 = np.random.choice(list(range(len(new_adjacencies))))

        new_adjacencies[idx1][idx2] = 1
        new_adjacencies[idx2][idx1] = 1

        return new_adjacencies

    _, adjacencies = ntm.evolve(initial_conditions=[1]*N, adjacency_matrix=adjacency_matrix,
                                activity_rule=activity_rule, connectivity_rule=connectivity_rule, timesteps=N)

    # NOTE: node self-links are not rendered
    ntm.animate_network(adjacencies, interval=250)