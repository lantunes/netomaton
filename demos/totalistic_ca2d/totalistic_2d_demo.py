import netomaton as ntm


if __name__ == '__main__':

    network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')

    initial_conditions = ntm.init_simple2d(60, 60)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=30,
                            activity_rule=ntm.rules.totalistic_ca(k=2, rule=126))

    ntm.plot_activities(trajectory, shape=(60, 60))
