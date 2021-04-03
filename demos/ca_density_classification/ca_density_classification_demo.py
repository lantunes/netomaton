import netomaton as ntm
import numpy as np


if __name__ == '__main__':
    # set r to 3, for a neighbourhood size of 7
    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(149, r=3)

    initial_conditions = np.random.randint(0, 2, 149)

    # Mitchell et al. discovered this rule using a Genetic Algorithm
    rule_number = 6667021275756174439087127638698866559

    print("density of 1s: %s" % (np.count_nonzero(initial_conditions) / 149))

    activities, adjacencies = ntm.evolve(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                         activity_rule=ntm.rules.binary_ca_rule(rule_number), timesteps=149)

    ntm.plot_grid(activities)
