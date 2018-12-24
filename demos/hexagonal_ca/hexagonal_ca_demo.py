import netomaton as ntm

if __name__ == '__main__':
    adjacencies = ntm.AdjacencyMatrix.cellular_automaton2d(60, 60, r=1, neighbourhood="Hex")

    initial_conditions = ntm.init_simple2d(60, 60)

    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=31,
                               activity_rule=lambda n, c, t: 1 if sum(n.activities) == 1 else n.current_activity)

    ntm.animate_hex(activities, shape=(60, 60), interval=150)
