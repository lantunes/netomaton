import netomaton as ntm
import numpy as np

"""
A growing version of the Erdős–Rényi model. We begin with a single unconnected node, and add a new node at each 
timestep, attaching it randomly to a node in the network. Nodes added earlier in the evolution have a greater 
probability of having a larger degree. Expected degree distribution: P(k) = 1 - e^(1-k), where k is the node degree. 
"""

if __name__ == "__main__":

    adjacency_matrix = [[1]]  # begin with a single-node network

    def activity_rule(ctx):
        # TODO this is a hack to get the activity list and adjacency matrix in sync
        curr_idx = ctx.node_index
        if ctx.timestep == curr_idx+1:
            ctx.insert(curr_idx, 1)
        # we aren't interested in the activity in this example, so the node's activity will always be the same
        return 1

    def connectivity_rule(cctx):
        new_adjacencies = [[i for i in x] for x in cctx.last_adjacencies]

        for row in new_adjacencies:
            row.append(0)
        new_adjacencies.append([0 for _ in range(len(new_adjacencies)+1)])

        new_idx = len(new_adjacencies) - 1
        connect_to = np.random.choice(list(range(len(new_adjacencies))))
        new_adjacencies[connect_to][new_idx] = 1
        new_adjacencies[new_idx][connect_to] = 1

        return new_adjacencies

    _, adjacencies = ntm.evolve(initial_conditions=[1], adjacency_matrix=adjacency_matrix,
                                activity_rule=activity_rule, connectivity_rule=connectivity_rule, timesteps=25)

    # NOTE: node self-links are not rendered
    ntm.animate_network(adjacencies, interval=250)
