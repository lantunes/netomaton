import netomaton as ntm

if __name__ == '__main__':
    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=200)

    initial_conditions = ntm.init_random(200)

    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=1000,
                               activity_rule=ntm.rules.nks_ca_rule(30))

    # calculate the average node entropy; the value will be ~0.999 in this case
    avg_node_entropy = ntm.average_node_entropy(activities)

    print(avg_node_entropy)
