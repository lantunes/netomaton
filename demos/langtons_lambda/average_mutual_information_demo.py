import netomaton as ntm

if __name__ == '__main__':
    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)

    initial_conditions = ntm.init_random(200)

    activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=1000,
                                 activity_rule=ntm.rules.nks_ca_rule_2(30))

    # calculate the average mutual information between a node and itself in the next time step
    avg_mutual_information = ntm.average_mutual_information(activities)

    print(avg_mutual_information)
