import netomaton as ntm

import matplotlib.pyplot as plt


if __name__ == '__main__':

    a = 2.5
    timesteps = 20

    adjacency_matrix = [[1]]
    initial_conditions = [0.5]

    def activity_rule(ctx):
        return a * ctx.current_activity * (1 - ctx.current_activity)


    activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                 activity_rule=activity_rule, timesteps=timesteps)

    # plot the position and velocity as a function of time
    y = [a[0] for a in activities]
    x = [n for n in range(1, timesteps+1)]
    fig, ax1 = plt.subplots()
    ax1.plot(x, y)
    ax1.set_xlabel('t')
    ax1.set_ylabel('x(t)')
    plt.show()
