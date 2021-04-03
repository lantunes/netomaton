import netomaton as ntm

if __name__ == '__main__':

    # NKS page 437 - Rule 214R

    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=63)

    # run the CA forward for 32 steps to get the initial condition for the next evolution
    initial_conditions = [0]*31 + [1] + [0]*31
    activities, _ = ntm.evolve(initial_conditions=initial_conditions, topology=adjacency_matrix,
                               activity_rule=ntm.ReversibleRule(ntm.rules.nks_ca_rule(214)),
                               past_conditions=[initial_conditions], timesteps=32)

    # use the last state of the CA as the initial, previous state for this evolution
    initial_conditions = activities[-2]
    activities, _ = ntm.evolve(initial_conditions=initial_conditions, topology=adjacency_matrix,
                               activity_rule=ntm.ReversibleRule(ntm.rules.nks_ca_rule(214)),
                               past_conditions=[activities[-1]], timesteps=62)

    ntm.plot_grid(activities)
