import netomaton as ntm

import matplotlib.pyplot as plt


if __name__ == '__main__':

    a = 2.5
    timesteps = 20

    network = ntm.topology.from_adjacency_matrix([[1]])
    initial_conditions = [0.5]

    def activity_rule(ctx):
        return a * ctx.current_activity * (1 - ctx.current_activity)


    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=timesteps)

    # plot the position and velocity as a function of time
    activities = ntm.get_activities_over_time_as_list(trajectory)
    y = [a[0] for a in activities]
    x = [n for n in range(1, timesteps+1)]
    fig, ax1 = plt.subplots()
    ax1.plot(x, y)
    ax1.set_xlabel('t')
    ax1.set_ylabel('x(t)')
    plt.show()
