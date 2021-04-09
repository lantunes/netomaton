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

    R_E = 80000  # resource absorption rate
    timesteps = 100
    width = 200
    height = 200

    # TODO could we define resource availability (i.e. 1) only at certain points (i.e. 0 everywhere else)
    #  and see if the model can solve something like the Traveling salesman problem? The resource sharing tracks
    #  generated would be the path taken

    initial_conditions = ntm.init_simple2d(width, height, val=R_E)

    model = ntm.FungalGrowthModel(R_E, width, height, initial_conditions, seed=20210408)

    activities, _ = ntm.evolve(topology=model.topology, initial_conditions=initial_conditions, timesteps=timesteps,
                               activity_rule=model.activity_rule, connectivity_rule=model.connectivity_rule,
                               update_order=model.update_order)

    activities_list = ntm.convert_activities_map_to_list(activities)
    ntm.animate(activities_list, shape=(width, height), interval=200, colormap="jet")
