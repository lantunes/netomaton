import netomaton as ntm
import numpy as np


if __name__ == '__main__':
    network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')

    initial_conditions = ntm.init_simple2d(60, 60)
    # the letter "E"
    initial_conditions[1709] = 1
    initial_conditions[1710] = 1
    initial_conditions[1711] = 1
    initial_conditions[1769] = 1
    initial_conditions[1829] = 1
    initial_conditions[1830] = 1
    initial_conditions[1831] = 1
    initial_conditions[1889] = 1
    initial_conditions[1949] = 1
    initial_conditions[1950] = 1
    initial_conditions[1951] = 1

    def activity_rule(ctx):
        return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 2

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=20,
                            activity_rule=activity_rule)

    ntm.animate_activities(trajectory, shape=(60, 60), interval=350)
