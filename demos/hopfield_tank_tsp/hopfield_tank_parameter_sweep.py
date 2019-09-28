import itertools
import numpy as np
import netomaton as ntm
import math


if __name__ == "__main__":

    As = [300, 400, 500, 600, 700]
    Bs = [300, 400, 500, 600, 700]
    Cs = [100, 150, 200, 250, 300]
    Ds = [300, 400, 500, 600, 700]
    ns = [10, 11, 12, 13, 14, 15, 16]
    ds = [1/1000, 1/10000, 1/100000, 1/1000000]
    ts = [1000, 2000]

    I = 10

    combinations = list(itertools.product(As, Bs, Cs, Ds, ns, ds, ts))

    print("number of combinations to try: %s" % len(combinations))

    points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88), (0.25, 0.99), (0.55, 0.25), (0.67, 0.78),
              (0.12, 0.35), (0.19, 0.89), (0.40, 0.23)]

    adjacency_matrix = [[1 for _ in range(100)] for _ in range(100)]

    for combination in combinations:
        A, B, C, D, n, dt, timesteps = combination
        lengths = []
        converged = []
        for i in range(I):

            tsp_net = ntm.HopfieldTankTSPNet(points, dt=dt, A=A, B=B, C=C, D=D, n=n)

            initial_conditions = [-0.022 + np.random.uniform(-0.1 * 0.02, 0.1 * 0.02) for _ in range(len(adjacency_matrix))]

            activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, tsp_net.activity_rule, timesteps=timesteps,
                                       parallel=True)

            permutation_matrix = tsp_net.get_permutation_matrix(activities)

            try:
                _, _, length = tsp_net.get_tour_graph(points, permutation_matrix)
                converged.append(1)
            except Exception as e:
                converged.append(0)
                continue

            lengths.append(length)

        result = combination, np.mean(lengths) if len(lengths) > 0 else math.nan, (sum(converged)/I)
        print(result)
