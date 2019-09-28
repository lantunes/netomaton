import netomaton as ntm

if __name__ == '__main__':
    adjacency_matrix = ntm.network.cellular_automaton2d(60, 60, r=1, neighbourhood="Hex")

    initial_conditions = ntm.init_simple2d(60, 60)

    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=31,
                               activity_rule=lambda ctx: 1 if sum(ctx.activities) == 1 else ctx.current_activity)

    ntm.animate_hex(activities, shape=(60, 60), interval=150)
