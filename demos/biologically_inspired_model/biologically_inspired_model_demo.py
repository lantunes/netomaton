import netomaton as ntm
import numpy as np


if __name__ == '__main__':
    """
    In this model, a network of agents are connected to eachother in a Euclidean lattice. Each agent 
    possesses a certain amount of "resource". An agent's resource can change by picking up resource from 
    a resource layer, and through the receipt of resource from its neighbours. 
    
    An agent represents a cell, and the links between agents represent the flow of resources between cells. (The 
    flow of resources is unidirectional only.)
    
    This implementation represents process "1", model "a", from the Smith et al. paper.
    """

    R_E = 80000  # resource absorption rate
    time_steps = 500
    width = 400
    height = 400
    num_agents = width*height
    d = 4  # the maximum node degree allowable
    np.random.seed(20210408)

    underlying_network = ntm.topology.table.lattice(dim=(1, width, height), periodic=True, first_label=0)
    links = set()
    for j, v in underlying_network.items():
        for i in v:
            links.add(frozenset((i, j)))
    initial_network = ntm.topology.table.disconnected(num_agents)

    print("initialized networks.")

    # TODO could we define resource availability (i.e. 1) only at certain points (i.e. 0 everywhere else)
    #  and see if the model can solve something like the Traveling salesman problem? The resource sharing tracks
    #  generated would be the path taken

    initial_conditions = ntm.init_simple2d(width, height, val=R_E)

    # a boolean matrix (flattened to a vector) representing the availability of resource to an agent
    resource_layer = [0 for i in range(num_agents)]
    # provide a single infinite resource at the same location as the initial agent
    resource_layer[np.nonzero(initial_conditions)[0][0]] = 1

    def activity_rule(ctx):
        # S_i = sum of neighbourhood activities times corresponding weights + available resources from resource layer
        neighbour_contribution = 0 if len(ctx.neighbour_labels) > 0 else ctx.current_activity
        for neighbour in ctx.neighbour_labels:
            neighbour_contribution += ctx.connection_states[neighbour][0]["weight"] * ctx.activities[neighbour]

        phi = 1 if ctx.current_activity > 0 else 0  # whether this agent is alive or dead
        L = resource_layer[ctx.node_label]  # whether resource is available to the agent from the resource layer
        resource_layer_contribution = R_E * phi * L

        S_i = neighbour_contribution + resource_layer_contribution
        return S_i

    def _degrees(degrees, label):
        if label not in degrees:
            return 0
        return degrees[label]

    def connectivity_rule(cctx):
        print("toplogy rule t: %s" % cctx.timestep)
        curr_map = cctx.connectivity_map
        curr_in_degrees, curr_out_degrees = ntm.get_node_degrees(curr_map)
        new_map = ntm.copy_connectivity_map(curr_map)
        for i, j in links:
            phi_S_i = 1 if cctx.activities[i] > 0 else 0
            phi_S_j = 1 if cctx.activities[j] > 0 else 0
            A_i_j = 1 if i in curr_map[j] else 0
            A_j_i = 1 if j in curr_map[i] else 0

            if A_i_j == 0 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 0:
                pass

            elif A_i_j == 0 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 1:
                p = 1 / (d - (_degrees(curr_in_degrees, j) + _degrees(curr_out_degrees, j)))
                if np.random.random() < p:
                    new_map[i][j] = [{}]

            elif A_i_j == 0 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 0:
                p = 1 / (d - (_degrees(curr_in_degrees, i) + _degrees(curr_out_degrees, i)))
                if np.random.random() < p:
                    new_map[j][i] = [{}]

            elif A_i_j == 0 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 1:
                p = 0.5
                if np.random.random() < p:
                    new_map[j][i] = [{}]
                else:
                    new_map[i][j] = [{}]

            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 0 and phi_S_j == 0:
                new_map[i][j] = [{}]
            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 0 and phi_S_j == 1:
                new_map[i][j] = [{}]
            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 1 and phi_S_j == 0:
                new_map[i][j] = [{}]
            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 1 and phi_S_j == 1:
                new_map[i][j] = [{}]

            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 0:
                new_map[j][i] = [{}]
            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 1:
                new_map[j][i] = [{}]
            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 0:
                new_map[j][i] = [{}]
            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 1:
                new_map[j][i] = [{}]

        _, new_out_degrees = ntm.get_node_degrees(new_map)
        for j, v in new_map.items():
            for i in v:
                new_map[j][i][0]["weight"] = 1 / _degrees(new_out_degrees, i)

        return new_map

    activities, _ = ntm.evolve(topology=initial_network, initial_conditions=initial_conditions, timesteps=time_steps,
                               activity_rule=activity_rule, connectivity_rule=connectivity_rule,
                               update_order=ntm.UpdateOrder.TOPOLOGY_FIRST)

    activities_list = ntm.convert_activities_map_to_list(activities)
    ntm.animate(activities_list, shape=(width, height), interval=200, colormap="jet")
