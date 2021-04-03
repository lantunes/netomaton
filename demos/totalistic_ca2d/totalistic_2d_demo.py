import netomaton as ntm


if __name__ == '__main__':

    adjacency_matrix = ntm.topology.adjacency.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')

    initial_conditions = ntm.init_simple2d(60, 60)

    activities, _ = ntm.evolve(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=30,
                               activity_rule=ntm.rules.totalistic_ca(k=2, rule=126))

    ntm.plot_grid(activities, shape=(60, 60))
