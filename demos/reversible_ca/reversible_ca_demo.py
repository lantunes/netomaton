from netomaton import *


if __name__ == '__main__':

    adjacencies = AdjacencyMatrix.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    r = ReversibleRule(initial_conditions, lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 90))

    activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=100,
                                        activity_rule=r.activity_rule)

    plot_grid(activities)
