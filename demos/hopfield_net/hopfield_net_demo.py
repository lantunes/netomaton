import netomaton as ntm


if __name__ == '__main__':
    # patterns for training
    zero = [
        0, 1, 1, 1, 0,
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        0, 1, 1, 1, 0]
    one = [
        0, 1, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0]
    two = [
        1, 1, 1, 0, 0,
        0, 0, 0, 1, 0,
        0, 0, 0, 1, 0,
        0, 1, 1, 0, 0,
        1, 0, 0, 0, 0,
        1, 1, 1, 1, 1]
    # replace the zeroes with -1 to make these vectors bipolar instead of binary
    one = [-1 if x == 0 else x for x in one]
    two = [-1 if x == 0 else x for x in two]
    zero = [-1 if x == 0 else x for x in zero]

    hopfield_net = ntm.HopfieldNet(n=30)

    hopfield_net.train([zero, one, two])

    # patterns to evaluate
    half_zero = [
        0, 1, 1, 1, 0,
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0]
    half_one = [
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0]
    half_two = [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 1, 1, 0, 0,
        1, 0, 0, 0, 0,
        1, 1, 1, 1, 1]
    half_zero = [-1 if x == 0 else x for x in half_zero]
    half_one = [-1 if x == 0 else x for x in half_one]
    half_two = [-1 if x == 0 else x for x in half_two]

    initial_conditions = half_two

    activities, adjacencies = ntm.evolve(initial_conditions, hopfield_net.adjacency_matrix,
                                         timesteps=hopfield_net.num_nodes * 7,
                                         activity_rule=hopfield_net.activity_rule)

    # view the weights, stored in the adjacency matrix
    # plot_grid(hopfield_net.adjacency_matrix)

    # view the time evolution of the Hopfield net as it completes the given pattern
    ntm.animate(activities[::hopfield_net.num_nodes], shape=(6, 5), interval=150)
