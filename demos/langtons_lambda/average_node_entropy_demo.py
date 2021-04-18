import netomaton as ntm

if __name__ == '__main__':
    network = ntm.topology.cellular_automaton(n=200)

    initial_conditions = ntm.init_random(200)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=1000,
                            activity_rule=ntm.rules.nks_ca_rule(30))

    # calculate the average node entropy; the value will be ~0.999 in this case
    avg_node_entropy = ntm.average_node_entropy(trajectory)

    print(avg_node_entropy)
