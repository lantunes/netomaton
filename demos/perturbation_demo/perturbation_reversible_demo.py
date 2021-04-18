import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    network = ntm.topology.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    def perturbed_rule(ctx):
        rule = ntm.rules.nks_ca_rule(90)
        if ctx.timestep % 10 == 0:
            return 1
        return rule(ctx)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100,
                            activity_rule=ntm.ReversibleRule(perturbed_rule), past_conditions=[initial_conditions])

    ntm.plot_activities(trajectory)
