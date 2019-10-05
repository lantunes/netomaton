import netomaton as ntm
import numpy as np

if __name__ == '__main__':

    adjacency_matrix = ntm.network.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    activities, adjacencies = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=100,
                                         activity_rule=ntm.ReversibleRule(ntm.rules.nks_ca_rule(90)),
                                         past_conditions=[initial_conditions])

    ntm.plot_grid(activities)
