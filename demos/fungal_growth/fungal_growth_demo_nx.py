import netomaton as ntm

if __name__ == '__main__':
    """
    In this model, a network of agents are connected to eachother in a Euclidean lattice. Each agent 
    possesses a certain amount of "resource". An agent's resource can change by picking up resource from 
    a resource layer, and through the receipt of resource from its neighbours. 

    An agent represents a cell, and the links between agents represent the flow of resources between cells. (The 
    flow of resources is unidirectional only.)

    This implementation represents process "1", model "a", from the paper:
    Smith, David MD, et al. "Network automata: Coupling structure and function in dynamic networks."
    Advances in Complex Systems 14.03 (2011): 317-339.
    """

    R_E = 80000.0  # resource absorption rate
    timesteps = 100
    width = 200
    height = 200

    initial_conditions = ntm.init_simple2d(width, height, val=R_E, dtype=float)

    model = ntm.FungalGrowthModel_NX(R_E, width, height, initial_conditions, seed=20210408)

    trajectory = ntm.evolve_nx(network=model.network, initial_conditions=initial_conditions, timesteps=timesteps,
                               activity_rule=model.activity_rule, topology_rule=model.topology_rule,
                               update_order=model.update_order)

    activities_list = ntm.get_activities_over_time_as_list(trajectory)
    ntm.animate(activities_list, shape=(width, height), interval=200, colormap="jet")
