import netomaton as ntm
import numpy as np


if __name__ == "__main__":

    points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88), (0.25, 0.99), (0.55, 0.25), (0.67, 0.78),
              (0.12, 0.35), (0.19, 0.89), (0.40, 0.23)]

    tsp_net = ntm.HopfieldTankTSPNet(points)

    adjacencies = tsp_net.adjacencies

    initial_conditions = [-0.022 + np.random.uniform(-0.1*.02, 0.1*.02) for _ in range(len(adjacencies))]

    activities, _ = ntm.evolve(initial_conditions, adjacencies, tsp_net.activity_rule, timesteps=30)

    # ntm.animate(activities, shape=(10, 10))

    permutation_matrix = tsp_net.get_permutation_matrix(activities)

    G, pos, length = tsp_net.get_tour_graph(points, permutation_matrix)

    print(length)

    tsp_net.plot_tour(G, pos)
