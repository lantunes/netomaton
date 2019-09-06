import netomaton as ntm
import numpy as np

if __name__ == '__main__':

    adjacencies = ntm.network.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    r = ntm.ReversibleRule(initial_conditions, lambda n, c, t: ntm.rules.nks_ca_rule(n, c, 90))

    activities, connectivities = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                                            activity_rule=r.activity_rule)

    ntm.plot_grid(activities)
