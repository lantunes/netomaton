import netomaton as ntm
from matplotlib.colors import ListedColormap


if __name__ == "__main__":

    network = ntm.topology.cellular_automaton2d(rows=13, cols=14, neighbourhood="Moore")

    initial_conditions = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
        2, 1, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3,
        0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
        2, 1, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3,
        0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=15,
                            activity_rule=ntm.rules.wireworld_rule)

    ntm.animate_activities(trajectory, shape=(13, 14), interval=120, show_grid=True, show_margin=False, scale=0.3,
                           colormap=ListedColormap(["black", "blue", "red", "yellow"]))
