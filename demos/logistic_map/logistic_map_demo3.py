import netomaton as ntm
import numpy as np

if __name__ == '__main__':

    """
    Generates a Poincaré plot for the logistic map.
    """

    timesteps = 1000
    num_nodes = 50
    growth_rates = np.linspace(3.6, 4.0, num_nodes)

    network = ntm.topology.disconnected(num_nodes)
    [network.add_edge(i, i, growth_rate=growth_rate) for i, growth_rate in enumerate(growth_rates)]

    initial_conditions = [0.5]*num_nodes

    def activity_rule(ctx):
        return ctx.edge_data(ctx.node_label, "growth_rate") * ctx.current_activity * (1 - ctx.current_activity)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=timesteps)

    activities = ntm.get_activities_over_time_as_list(trajectory)

    # create the Poincaré plot
    activities = np.array(activities)
    ntm.poincare_plot(activities=[activities[:, i] for i in range(num_nodes)],
                      timesteps=int((timesteps/2)),
                      xlabel="Population", ylabel="Population(t + 1)",
                      xlim=(0.25, 0.75), ylim=(0.8, 1.01))
