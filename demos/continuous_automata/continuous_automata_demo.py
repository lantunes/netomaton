import math
import netomaton as ntm


if __name__ == '__main__':

    network = ntm.topology.cellular_automaton(n=200)

    initial_conditions = [0.0]*100 + [1.0] + [0.0]*99

    # NKS page 157
    def activity_rule(ctx):
        activities = ctx.neighbourhood_activities
        result = (sum(activities) / len(activities)) * (3 / 2)
        frac, whole = math.modf(result)
        return frac

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=150)

    ntm.plot_activities(trajectory)
