import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    adjacencies = ntm.network.cellular_automaton(n=200)
    initial_conditions = [0] * 100 + [1] + [0] * 99

    def perturb(c, a, t):
        """
        Mutates the value of the cell with index 100 at each timestep, making it either 0 or 1 randomly.
        """
        if c == 100:
            return np.random.randint(2)
        return a

    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                               activity_rule=lambda n, c, t: ntm.rules.nks_ca_rule(n, c, 30),
                               perturbation=perturb)

    ntm.plot_grid(activities)
