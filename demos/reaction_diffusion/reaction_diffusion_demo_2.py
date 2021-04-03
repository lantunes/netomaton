import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    adjacency_matrix = ntm.topology.adjacency.cellular_automaton2d(rows=100, cols=100, r=1, neighbourhood='von Neumann')

    # create perturbation 'dots' in the center of uniform conditions
    initial_conditions = np.array([(1, 0) for i in range(100 * 100)], dtype='d, d').reshape(100, 100)
    n = 100

    a, b = 50, 50  # coordinates of dot center
    r = 10  # the dot radius
    y, x = np.ogrid[-a:n - a, -b:n - b]
    mask = x * x + y * y <= r * r
    initial_conditions[mask] = (0.5, 0.25)

    a, b = 30, 30  # coordinates of dot center
    r = 10  # the dot radius
    y, x = np.ogrid[-a:n - a, -b:n - b]
    mask = x * x + y * y <= r * r
    initial_conditions[mask] = (0.5, 0.25)

    a, b = 75, 75  # coordinates of dot center
    r = 10  # the dot radius
    y, x = np.ogrid[-a:n - a, -b:n - b]
    mask = x * x + y * y <= r * r
    initial_conditions[mask] = (0.5, 0.25)

    initial_conditions = initial_conditions.reshape(100 * 100).tolist()

    r_u = 0.02
    r_v = 0.01
    f = 0.01
    k = 0.05

    def react_diffuse(ctx):
        prev_u = ctx.current_activity[0]
        prev_v = ctx.current_activity[1]

        neighbourhood_u = [ctx.neighbourhood_activities[i][0] for i, idx in enumerate(ctx.neighbour_labels) if
                           idx != ctx.node_label]
        neighbourhood_v = [ctx.neighbourhood_activities[i][1] for i, idx in enumerate(ctx.neighbour_labels) if
                           idx != ctx.node_label]

        diffusion_u = sum(neighbourhood_u) - (4 * prev_u)
        diffusion_v = sum(neighbourhood_v) - (4 * prev_v)

        inter_u = (-prev_u * prev_v ** 2) + f * (1 - prev_u)
        inter_v = (prev_u * prev_v ** 2) - (k) * prev_v

        new_u = prev_u + (r_u * diffusion_u) + inter_u
        new_v = prev_v + (r_v * diffusion_v) + inter_v

        return new_u, new_v

    activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                 activity_rule=react_diffuse, timesteps=3000)

    # we want to visualize the concentrations of U only
    activities = [[j[0] for j in i] for i in activities]

    ntm.animate(activities, shape=(100, 100), colormap='RdYlBu', vmin=0.2, interval=25)
