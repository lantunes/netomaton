from netomaton import *


# set r to 3, for a neighbourhood size of 7
adjacencies = AdjacencyMatrix.cellular_automaton(149, r=3)

initial_conditions = np.random.randint(0, 2, 149)

# Mitchell et al. discovered this rule using a Genetic Algorithm
rule_number = 6667021275756174439087127638698866559

print("density of 1s: %s" % (np.count_nonzero(initial_conditions) / 149))

activities, connectivities = evolve(adjacencies, initial_conditions, timesteps=149,
                                    activity_rule=lambda n, c, t: ActivityRule.binary_ca_rule(n, c, rule_number))

plot_grid(activities)
