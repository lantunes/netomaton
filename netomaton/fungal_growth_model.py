import netomaton as ntm
import numpy as np
from collections import defaultdict


class FungalGrowthModel:
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
    def __init__(self, R_E, width, height, initial_conditions, seed=None, verbose=True):
        """
        :param R_E: resource absorption rate
        :param width: an integer representing the width of the grid of agents
        :param height: an integer representing the height of the grid of agents
        :param initial_conditions: a list of integers representing the initial conditions, in terms of the starting
                                   amount of resource for each agent
        :param seed: integer, random_state, or None (default); a random seed to use for random number generation
        :param verbose: whether to print progress statements to the console (default is True)
        """
        self._R_E = R_E
        self._d = 4  # the maximum node degree allowable
        if seed:
            np.random.seed(seed)
        self._verbose = verbose

        num_agents = width * height

        underlying_network = ntm.topology.table.lattice(dim=(1, width, height), periodic=True, first_label=0)
        self._links = set()
        for j, v in underlying_network.items():
            for i in v:
                self._links.add(frozenset((i, j)))
        self._initial_network = ntm.topology.table.disconnected(num_agents)

        # a boolean matrix (flattened to a vector) representing the availability of resource to an agent
        self._resource_layer = [0 for i in range(num_agents)]
        # provide a single infinite resource at the same location as the initial agent(s)
        for nz in np.nonzero(initial_conditions)[0]:
            self._resource_layer[nz] = 1

        if self._verbose:
            print("initialization complete")

    def connectivity_rule(self, cctx):
        if self._verbose:
            print("topology rule - t: %s" % cctx.timestep)
        curr_map = cctx.connectivity_map
        curr_in_degrees, curr_out_degrees = ntm.get_node_degrees(curr_map)
        new_map = ntm.copy_connectivity_map(curr_map)
        new_out_degrees = defaultdict(int)
        for i, j in self._links:
            phi_S_i = 1 if cctx.activities[i] > 0 else 0
            phi_S_j = 1 if cctx.activities[j] > 0 else 0
            A_i_j = 1 if i in curr_map[j] else 0
            A_j_i = 1 if j in curr_map[i] else 0

            if A_i_j == 0 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 0:
                pass

            elif A_i_j == 0 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 1:
                p = 1 / (self._d - (self._degrees(curr_in_degrees, j) + self._degrees(curr_out_degrees, j)))
                if np.random.random() < p:
                    new_map[i][j] = [{}]
                    new_out_degrees[j] += 1

            elif A_i_j == 0 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 0:
                p = 1 / (self._d - (self._degrees(curr_in_degrees, i) + self._degrees(curr_out_degrees, i)))
                if np.random.random() < p:
                    new_map[j][i] = [{}]
                    new_out_degrees[i] += 1

            elif A_i_j == 0 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 1:
                p = 0.5
                if np.random.random() < p:
                    new_map[j][i] = [{}]
                    new_out_degrees[i] += 1
                else:
                    new_map[i][j] = [{}]
                    new_out_degrees[j] += 1

            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 0 and phi_S_j == 0:
                new_map[i][j] = [{}]
                new_out_degrees[j] += 1
            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 0 and phi_S_j == 1:
                new_map[i][j] = [{}]
                new_out_degrees[j] += 1
            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 1 and phi_S_j == 0:
                new_map[i][j] = [{}]
                new_out_degrees[j] += 1
            elif A_i_j == 0 and A_j_i == 1 and phi_S_i == 1 and phi_S_j == 1:
                new_map[i][j] = [{}]
                new_out_degrees[j] += 1

            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 0:
                new_map[j][i] = [{}]
                new_out_degrees[i] += 1
            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 0 and phi_S_j == 1:
                new_map[j][i] = [{}]
                new_out_degrees[i] += 1
            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 0:
                new_map[j][i] = [{}]
                new_out_degrees[i] += 1
            elif A_i_j == 1 and A_j_i == 0 and phi_S_i == 1 and phi_S_j == 1:
                new_map[j][i] = [{}]
                new_out_degrees[i] += 1

        for j, v in new_map.items():
            for i in v:
                new_map[j][i][0]["weight"] = 1 / self._degrees(new_out_degrees, i)

        return new_map

    def activity_rule(self, ctx):
        # S_i = sum of neighbourhood activities times corresponding weights + available resources from resource layer
        neighbour_contribution = 0 if len(ctx.neighbour_labels) > 0 else ctx.current_activity
        for neighbour in ctx.neighbour_labels:
            neighbour_contribution += ctx.connection_states[neighbour][0]["weight"] * ctx.activities[neighbour]

        phi = 1 if ctx.current_activity > 0 else 0  # whether this agent is alive or dead
        L = self._resource_layer[ctx.node_label]  # whether resource is available to the agent from the resource layer
        resource_layer_contribution = self._R_E * phi * L

        S_i = neighbour_contribution + resource_layer_contribution
        return S_i

    @property
    def topology(self):
        return self._initial_network

    @property
    def update_order(self):
        return ntm.UpdateOrder.TOPOLOGY_FIRST

    @staticmethod
    def _degrees(degrees, label):
        if label not in degrees:
            return 0
        return degrees[label]
