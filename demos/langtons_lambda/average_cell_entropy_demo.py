import netomaton as ntm

if __name__ == '__main__':
    adjacencies = ntm.AdjacencyMatrix.cellular_automaton(n=200)

    initial_conditions = ntm.init_random(200)

    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=1000,
                               activity_rule=lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 30))

    # calculate the average cell entropy; the value will be ~0.999 in this case
    avg_cell_entropy = ntm.average_cell_entropy(activities)

    print(avg_cell_entropy)
