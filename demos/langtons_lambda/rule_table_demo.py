import netomaton as ntm

if __name__ == '__main__':
    rule_table, actual_lambda, quiescent_state = ntm.random_rule_table(lambda_val=0.37, k=4, r=2,
                                                                       strong_quiescence=True, isotropic=True)

    network = ntm.topology.cellular_automaton(n=128, r=2)

    initial_conditions = ntm.init_random(128, k=4, n_randomized=20)

    # evolve the cellular automaton for 200 time steps
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=200,
                            activity_rule=ntm.table_rule(rule_table))

    ntm.plot_activities(trajectory)
