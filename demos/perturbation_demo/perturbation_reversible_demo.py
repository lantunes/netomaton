from netomaton import *


if __name__ == '__main__':

    adjacencies = AdjacencyMatrix.cellular_automaton(n=200)

    initial_conditions = np.random.randint(0, 2, 200)

    def perturbed_rule(n, c, t):
        a = ActivityRule.nks_ca_rule(n, c, 90)
        if t % 10 == 0:
            return 1
        return a

    r = ReversibleRule(initial_conditions, perturbed_rule)

    activities, _ = evolve(initial_conditions, adjacencies, timesteps=100,
                                        activity_rule=r.activity_rule)

    plot_grid(activities)
