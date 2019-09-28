import netomaton as ntm

if __name__ == '__main__':
    adjacencies = ntm.network.cellular_automaton(n=200)

    initial_conditions = ntm.init_random(200)

    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=1000,
                               activity_rule=lambda ctx: ntm.rules.nks_ca_rule(ctx, 30))

    # calculate the average mutual information between a cell and itself in the next time step
    avg_mutual_information = ntm.average_mutual_information(activities)

    print(avg_mutual_information)
