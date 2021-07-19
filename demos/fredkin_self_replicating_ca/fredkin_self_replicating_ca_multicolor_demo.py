import netomaton as ntm
import numpy as np


if __name__ == '__main__':
    network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='von Neumann')

    initial_conditions = ntm.init_simple2d(60, 60)
    # the letter "E"
    initial_conditions[1709] = 0
    initial_conditions[1710] = 1
    initial_conditions[1711] = 2
    initial_conditions[1769] = 3
    initial_conditions[1829] = 4
    initial_conditions[1830] = 5
    initial_conditions[1831] = 6
    initial_conditions[1889] = 7
    initial_conditions[1949] = 8
    initial_conditions[1950] = 9
    initial_conditions[1951] = 10

    def activity_rule(ctx):
        return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 11

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=23,
                            activity_rule=activity_rule)

    ntm.animate_activities(trajectory, shape=(60, 60), interval=350, colormap='viridis')
