import netomaton as ntm

if __name__ == '__main__':

    # NKS page 437 - Rule 214R

    network = ntm.topology.cellular_automaton(n=63)

    # run the CA forward for 32 steps to get the initial condition for the next evolution
    initial_conditions = [0]*31 + [1] + [0]*31
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=ntm.ReversibleRule(ntm.rules.nks_ca_rule(214)),
                            past_conditions=[initial_conditions], timesteps=32)

    # use the last state of the CA as the initial, previous state for this evolution
    activities = ntm.get_activities_over_time_as_list(trajectory)
    initial_conditions = activities[-2]
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=ntm.ReversibleRule(ntm.rules.nks_ca_rule(214)),
                            past_conditions=[activities[-1]], timesteps=62)

    ntm.plot_activities(trajectory)
