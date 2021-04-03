import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    def perturbed_rule(ctx):
        rule = ntm.rules.nks_ca_rule(90)
        if ctx.timestep % 10 == 0:
            return 1
        return rule(ctx)

    activities, _ = ntm.evolve(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=100,
                               activity_rule=ntm.ReversibleRule(perturbed_rule), past_conditions=[initial_conditions])

    ntm.plot_grid(activities)
