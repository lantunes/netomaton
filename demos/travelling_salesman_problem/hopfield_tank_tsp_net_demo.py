import netomaton as ntm
import numpy as np


if __name__ == "__main__":

    """
    dt=1/1000, A=500, B=500, C=200, D=500, n=15/100, timesteps=1000
    tour distance = 2.776312476334959
    tour distance = 2.5454480605753607
    tour distance = 2.6470181953022607
    tour distance = 2.7076916516030143
    tour distance = 2.8044558496491274
    tour distance = 3.0918504517445644
    (converges to a correct permutation matrix about 15-30% of the time)
    
    dt=1/1000000, A=500, B=500, C=200, D=500, n=15/100, timesteps=1000
    tour distance = 3.376541788178572
    tour distance = 3.104700743771862
    tour distance = 3.2040085435175283
    tour distance = 3.0234128207371707
    tour distance = 3.2339964755835386
    (converges to a correct permutation matrix about 30-50% of the time)
    """

    points = [(0, 1), (0.23, 0.5), (0.6, 0.77), (0.33, 0.88), (0.25, 0.99), (0.55, 0.25), (0.67, 0.78),
              (0.12, 0.35), (0.19, 0.89), (0.40, 0.23)]

    tsp_net = ntm.HopfieldTankTSPNet(points, dt=1/1000000, A=500, B=500, C=200, D=500, n=15/100)

    adjacencies = tsp_net.adjacencies

    # -0.022 was chosen so that the sum of V for all cells is 10; some noise is added to break the symmetry
    initial_conditions = [-0.022 + np.random.uniform(-0.1*0.02, 0.1*0.02) for _ in range(len(adjacencies))]

    activities, _ = ntm.evolve(initial_conditions, adjacencies, tsp_net.activity_rule, timesteps=1000, parallel=True)

    ntm.animate(activities, shape=(10, 10))

    permutation_matrix = tsp_net.get_permutation_matrix(activities)
    print(permutation_matrix)

    G, pos, length = tsp_net.get_tour_graph(points, permutation_matrix)

    print(length)

    tsp_net.plot_tour(G, pos)
