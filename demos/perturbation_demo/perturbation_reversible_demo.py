import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    adjacency_matrix = ntm.network.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    def perturbed_rule(ctx):
        a = ntm.rules.nks_ca_rule(ctx, 90)
        if ctx.timestep % 10 == 0:
            return 1
        return a

    r = ntm.ReversibleRule(perturbed_rule)

    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=100,
                               activity_rule=r.activity_rule, past_conditions=[initial_conditions])

    ntm.plot_grid(activities)
