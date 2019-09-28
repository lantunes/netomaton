import netomaton as ntm

if __name__ == '__main__':

    # NKS page 437 - Rule 214R

    adjacency_matrix = ntm.network.cellular_automaton(n=63)

    # run the CA forward for 32 steps to get the initial condition for the next evolution
    initial_conditions = [0]*31 + [1] + [0]*31
    r = ntm.ReversibleRule(lambda ctx: ntm.rules.nks_ca_rule(ctx, 214))
    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=32, activity_rule=r.activity_rule,
                               past_conditions=[initial_conditions])

    # use the last state of the CA as the initial, previous state for this evolution
    r = ntm.ReversibleRule(lambda ctx: ntm.rules.nks_ca_rule(ctx, 214))
    initial_conditions = activities[-2]
    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=62, activity_rule=r.activity_rule,
                               past_conditions=[activities[-1]])

    ntm.plot_grid(activities)
