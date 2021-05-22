import netomaton as ntm

if __name__ == '__main__':
    """
    The Collatz Conjecture states that by iteratively applying a particular rule to successive numbers, beginning from
    any number, the result will eventually be 1. This demo illustrates the use of the input function to terminate
    an evolution dynamically, based on the value of the activities.
    
    See: https://en.wikipedia.org/wiki/Collatz_conjecture
    """

    network = ntm.topology.from_adjacency_matrix([[1]])

    def activity_rule(ctx):
        n = ctx.current_activity
        if n % 2 == 0:
            # number is even
            return n / 2
        else:
            return  3*n + 1

    def input(t, activities, n):
        if activities[0] == 1:
            return None
        return 1

    initial_conditions = [4103453]

    trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions,
                            activity_rule=activity_rule, input=input)

    activities = ntm.get_activities_over_time_as_list(trajectory)

    # print the numbers produced
    print([a[0] for a in activities])

    # convert the numbers to binary lists and left-pad with zeroes, so we can plot them
    activities = ntm.binarize_for_plotting(activities)

    ntm.plot_grid(activities)
