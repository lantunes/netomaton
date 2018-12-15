import netomaton as ntm

if __name__ == '__main__':
    rule_table, actual_lambda, quiescent_state = ntm.random_rule_table(lambda_val=0.0, k=4, r=2,
                                                                       strong_quiescence=True, isotropic=True)

    lambda_vals = [0.15, 0.37, 0.75]
    ca_list = []
    titles = []
    for i in range(0, 3):
        adjacencies = ntm.AdjacencyMatrix.cellular_automaton(n=128, r=2)

        initial_conditions = ntm.init_random(128, k=4)

        rule_table, actual_lambda = ntm.table_walk_through(rule_table, lambda_vals[i], k=4, r=2,
                                                           quiescent_state=quiescent_state, strong_quiescence=True)
        print(actual_lambda)

        # evolve the cellular automaton for 200 time steps
        activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=200,
                                   activity_rule=lambda n, c, t: ntm.table_rule(n, rule_table))

        ca_list.append(activities)
        avg_cell_entropy = ntm.average_cell_entropy(activities)
        avg_mutual_information = ntm.average_mutual_information(activities)
        titles.append(r'$\lambda$ = %s, $\widebar{H}$ = %s, $\widebar{I}$ = %s' %
                      (lambda_vals[i], "{:.4}".format(avg_cell_entropy), "{:.4}".format(avg_mutual_information)))

    ntm.plot_grid_multiple(ca_list, titles)
