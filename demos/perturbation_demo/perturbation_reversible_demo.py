import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    adjacencies = ntm.network.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    def perturbed_rule(n, c, t):
        a = ntm.ActivityRule.nks_ca_rule(n, c, 90)
        if t % 10 == 0:
            return 1
        return a

    r = ntm.ReversibleRule(initial_conditions, perturbed_rule)

    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                               activity_rule=r.activity_rule)

    ntm.plot_grid(activities)
