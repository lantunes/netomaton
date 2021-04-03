import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)
    initial_conditions = [0] * 100 + [1] + [0] * 99

    def perturb(pctx):
        """
        Mutates the value of the node with index 100 at each timestep, making it either 0 or 1 randomly.
        """
        if pctx.node_index == 100:
            return np.random.randint(2)
        return pctx.node_activity

    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=100,
                               activity_rule=ntm.rules.nks_ca_rule(30),
                               perturbation=perturb)

    ntm.plot_grid(activities)
