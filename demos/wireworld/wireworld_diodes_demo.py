import netomaton as ntm
from matplotlib.colors import ListedColormap


if __name__ == "__main__":

    adjacency_matrix = ntm.network.cellular_automaton2d(rows=13, cols=14, neighbourhood="Moore")

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

    def wireworld(ctx):
        if ctx.current_activity == 0:  # empty
            return 0
        if ctx.current_activity == 1:  # electron head
            return 2
        if ctx.current_activity == 2:  # electron tail
            return 3
        if ctx.current_activity == 3:  # conductor
            electron_head_count = ctx.activities.count(1)
            return 1 if electron_head_count == 1 or electron_head_count == 2 else 3

    activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, activity_rule=wireworld, timesteps=15)

    ntm.animate(activities, shape=(13, 14), interval=120, show_grid=True,
                colormap=ListedColormap(["black", "blue", "red", "yellow"]))
