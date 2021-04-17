import netomaton as ntm


if __name__ == '__main__':

    network = ntm.topology.cellular_automaton(n=200)

    initial_conditions = [0] * 100 + [1] + [0] * 99

    trajectory = ntm.evolve_n2(network=network, initial_conditions=initial_conditions,
                               activity_rule=ntm.rules.nks_ca_rule(30), timesteps=100)

    ntm.plot_activities(trajectory)
