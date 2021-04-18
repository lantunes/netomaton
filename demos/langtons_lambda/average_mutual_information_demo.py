import netomaton as ntm

if __name__ == '__main__':
    network = ntm.topology.cellular_automaton(n=200)

    initial_conditions = ntm.init_random(200)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=1000,
                            activity_rule=ntm.rules.nks_ca_rule(30))

    # calculate the average mutual information between a node and itself in the next time step
    avg_mutual_information = ntm.average_mutual_information(trajectory)

    print(avg_mutual_information)
