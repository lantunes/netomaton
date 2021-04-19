import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    """
    Generates a Bifurcation plot for the logistic map.
    """

    timesteps = 200
    num_nodes = 1000
    growth_rates = np.linspace(0.0, 4.0, num_nodes)

    network = ntm.topology.disconnected(num_nodes)
    [network.add_edge(i, i, weight=growth_rate) for i, growth_rate in enumerate(growth_rates)]

    initial_conditions = [0.5]*num_nodes

    def activity_rule(ctx):
        return ctx.edge_data(ctx.node_label, "weight") * ctx.current_activity * (1 - ctx.current_activity)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=timesteps)

    activities = np.array(ntm.get_activities_over_time_as_list(trajectory))

    y = []
    for i in range(num_nodes):
        y.append(np.unique(activities[:, i][-100:]))

    x = growth_rates
    for x_e, y_e in zip(x, y):
        plt.scatter([x_e] * len(y_e), y_e, color="b", s=1)
    plt.xlabel("Growth rate")
    plt.ylabel("Population")
    plt.show()
