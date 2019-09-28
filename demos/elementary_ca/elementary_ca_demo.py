import netomaton as ntm


if __name__ == '__main__':

    adjacencies = ntm.network.cellular_automaton(n=200)

    initial_conditions = [0] * 100 + [1] + [0] * 99

    activities, connectivities = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                                            activity_rule=lambda ctx: ntm.rules.nks_ca_rule(ctx, 30))

    ntm.plot_grid(activities)
