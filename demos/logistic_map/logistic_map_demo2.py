import netomaton as ntm
import numpy as np

if __name__ == '__main__':

    """
    Generates a Bifurcation plot for the logistic map.
    """

    timesteps = 200
    num_nodes = 1000
    growth_rates = np.linspace(0.0, 4.0, num_nodes)

    network = ntm.topology.disconnected(num_nodes)
    [network.add_edge(i, i, growth_rate=growth_rate) for i, growth_rate in enumerate(growth_rates)]

    initial_conditions = [0.5]*num_nodes

    def activity_rule(ctx):
        return ctx.edge_data(ctx.node_label, "growth_rate") * ctx.current_activity * (1 - ctx.current_activity)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=timesteps)

    activities = ntm.get_activities_over_time_as_list(trajectory)

    # create the bifurcation plot
    activities = np.array(activities)
    ntm.bifurcation_plot(x=growth_rates, timesteps=int((timesteps/2)),
                         trajectories=[activities[:, i] for i in range(num_nodes)],
                         xlabel="Growth rate", ylabel="Population")
