import netomaton as ntm

if __name__ == '__main__':
    adjacency_matrix = ntm.network.cellular_automaton2d(60, 60, r=1, neighbourhood="Hex")

    initial_conditions = ntm.init_simple2d(60, 60)

    def activity_rule(ctx):
        return 1 if sum(ctx.neighbourhood_activities) == 1 else ctx.current_activity

    activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix, timesteps=31,
                                 activity_rule=activity_rule)

    ntm.animate_hex(activities, shape=(60, 60), interval=150)
