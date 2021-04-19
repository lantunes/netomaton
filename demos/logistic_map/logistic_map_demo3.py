import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    """
    Generates a Poincaré plot for the logistic map.
    """

    timesteps = 1000
    num_nodes = 50
    growth_rates = np.linspace(3.6, 4.0, num_nodes)

    network = ntm.topology.disconnected(num_nodes)
    [network.add_edge(i, i, weight=growth_rate) for i, growth_rate in enumerate(growth_rates)]

    initial_conditions = [0.5]*num_nodes

    def activity_rule(ctx):
        return ctx.edge_data(ctx.node_label, "weight") * ctx.current_activity * (1 - ctx.current_activity)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=timesteps)

    activities = np.array(ntm.get_activities_over_time_as_list(trajectory))

    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle(color=[cm(1. * i / num_nodes) for i in range(num_nodes)])
    for i in range(num_nodes):
        x = []
        y = []
        keep = int((timesteps/2))
        for t in range(keep - 1):
            x.append(activities[:, i][-keep:][t])
            y.append(activities[:, i][-keep:][t+1])

        plt.scatter(x, y, s=1)

    plt.xlim(0.25, 0.75)
    plt.ylim(0.8, 1.01)
    plt.xlabel("Population")
    plt.ylabel("Population(t + 1)")
    plt.show()