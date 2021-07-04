import netomaton as ntm


if __name__ == '__main__':
    network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='von Neumann')
    initial_conditions = ntm.init_simple2d(60, 60)
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=30,
                            activity_rule=ntm.rules.totalistic_ca(k=2, rule=26))
    # the evolution of a 2D cellular automaton can be animated
    ntm.animate_activities(trajectory, shape=(60, 60), interval=150)

    network = ntm.topology.cellular_automaton(n=200)
    initial_conditions = [0] * 100 + [1] + [0] * 99
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100,
                            activity_rule=ntm.rules.nks_ca_rule(30))
    # the evolution of a 1D cellular automaton can be animated
    ntm.animate_activities(trajectory, shape=(200,))

    network = ntm.topology.cellular_automaton(n=225)
    initial_conditions = [0] * 112 + [1] + [0] * 112
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100,
                            activity_rule=ntm.rules.nks_ca_rule(30))
    # a 1D cellular automaton can be rendered an animated as if it were a 2D cellular automaton
    ntm.animate_activities(trajectory, shape=(15, 15), interval=100)
