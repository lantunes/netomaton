import netomaton as ntm


if __name__ == '__main__':

    adj = ntm.topology.adjacency.cellular_automaton(n=200)
    # TODO move into function
    network = ntm.Network()
    for i, row in enumerate(adj):
        for j, val in enumerate(row):
            if val == 1:
                network.add_edge(i, j)

    initial_conditions = [0] * 100 + [1] + [0] * 99

    trajectory = ntm.evolve_n2(network=network, initial_conditions=initial_conditions,
                               activity_rule=ntm.rules.nks_ca_rule(30), timesteps=100)

    ntm.plot_activities_n2(trajectory)
