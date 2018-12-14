import math
from netomaton import *


if __name__ == '__main__':

    adjacencies = AdjacencyMatrix.cellular_automaton(n=200)

    initial_conditions = [0.0]*100 + [1.0] + [0.0]*99

    # NKS page 157
    def activity_rule(n, c, t):
        activities = n.activities
        result = (sum(activities) / len(activities)) * (3 / 2)
        frac, whole = math.modf(result)
        return frac

    activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=150,
                                        activity_rule=activity_rule)

    plot_grid(activities)
