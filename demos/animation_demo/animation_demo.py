import netomaton as ntm


if __name__ == '__main__':
    adjacencies = ntm.AdjacencyMatrix.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='von Neumann')
    initial_conditions = ntm.init_simple2d(60, 60)
    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=30,
                               activity_rule=lambda n, c, t: ntm.ActivityRule.totalistic_ca(n, k=2, rule=26))
    # the evolution of a 2D cellular automaton can be animated
    ntm.animate(activities, shape=(60, 60), interval=150)

    adjacencies = ntm.AdjacencyMatrix.cellular_automaton(n=200)
    initial_conditions = [0] * 100 + [1] + [0] * 99
    activities, connectivities = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                                            activity_rule=lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 30))
    # the evolution of a 1D cellular automaton can be animated
    ntm.animate(activities, shape=(200,))

    adjacencies = ntm.AdjacencyMatrix.cellular_automaton(n=225)
    initial_conditions = [0] * 112 + [1] + [0] * 112
    activities, connectivities = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                                            activity_rule=lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 30))
    # a 1D cellular automaton can be rendered an animated as if it were a 2D cellular automaton
    ntm.animate(activities, shape=(15, 15), interval=100)