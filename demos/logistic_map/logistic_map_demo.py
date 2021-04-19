import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    timesteps = 20
    growth_rates = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

    # We'll create a network of fully disconnected nodes, except for a connection to
    # from a node to itself, and a weight on that self-loop that represents the growth rate.
    # Thus, we are simply setting up a node for each growth rate, so that we can evolve the
    # system with different growth rates at the same time.
    network = ntm.topology.disconnected(len(growth_rates))
    [network.add_edge(i, i, weight=growth_rate) for i, growth_rate in enumerate(growth_rates)]

    # all nodes have the same population value at the start
    initial_conditions = [0.5]*len(growth_rates)

    def activity_rule(ctx):
        return ctx.edge_data(ctx.node_label, "weight") * ctx.current_activity * (1 - ctx.current_activity)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=timesteps)

    activities = np.array(ntm.get_activities_over_time_as_list(trajectory))

    fig, ax = plt.subplots()
    x = [n for n in range(1, timesteps + 1)]
    ax.plot(x, activities[:, 0], label=0.5)
    ax.plot(x, activities[:, 1], label=1.0)
    ax.plot(x, activities[:, 2], label=1.5)
    ax.plot(x, activities[:, 3], label=2.0)
    ax.plot(x, activities[:, 4], label=2.5)
    ax.plot(x, activities[:, 5], label=3.0)
    ax.plot(x, activities[:, 6], label=3.5)
    ax.set_xlabel('t')
    ax.set_ylabel('x(t)')
    ax.legend(title="Growth rate", bbox_to_anchor=(1.04, 1))
    plt.tight_layout(rect=[0, 0, 0.95, 1])
    plt.show()
