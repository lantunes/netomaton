import netomaton as ntm


if __name__ == '__main__':

    adjacencies = ntm.AdjacencyMatrix.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')

    initial_conditions = ntm.init_simple2d(60, 60)

    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=30,
                               activity_rule=lambda n, c, t: ntm.ActivityRule.totalistic_ca(n, k=2, rule=126))

    ntm.plot_grid(activities, shape=(60, 60))
