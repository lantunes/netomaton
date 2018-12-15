import netomaton as ntm

if __name__ == '__main__':

    # NKS page 437 - Rule 214R

    adjacencies = ntm.AdjacencyMatrix.cellular_automaton(n=63)

    # run the CA forward for 32 steps to get the initial condition for the next evolution
    initial_conditions = [0]*31 + [1] + [0]*31
    r = ntm.ReversibleRule(initial_conditions, lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 214))
    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=32, activity_rule=r.activity_rule)

    # use the last state of the CA as the initial, previous state for this evolution
    r = ntm.ReversibleRule(activities[-1], lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 214))
    initial_conditions = activities[-2]
    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=62, activity_rule=r.activity_rule)

    ntm.plot_grid(activities)
