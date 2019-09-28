import math
import netomaton as ntm


if __name__ == '__main__':

    adjacencies = ntm.network.cellular_automaton(n=200)

    initial_conditions = [0.0]*100 + [1.0] + [0.0]*99

    # NKS page 157
    def activity_rule(ctx):
        activities = ctx.activities
        result = (sum(activities) / len(activities)) * (3 / 2)
        frac, whole = math.modf(result)
        return frac

    activities, connectivities = ntm.evolve(initial_conditions, adjacencies, timesteps=150,
                                            activity_rule=activity_rule)

    ntm.plot_grid(activities)
