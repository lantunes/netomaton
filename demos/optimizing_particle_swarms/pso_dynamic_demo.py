import netomaton as ntm
import numpy as np
import math


def f(x):
    # n-dimensional sphere function
    return np.sum(x ** 2)


def p_decay(timestep, initial_p=0.9, drop=0.9, timesteps_drop=10.0):
    return initial_p * math.pow(drop, math.floor((1+timestep)/timesteps_drop))


if __name__ == '__main__':
    """
    See: https://en.wikipedia.org/wiki/Particle_swarm_optimization#Algorithm

    Here we search for the minimum of the 30-dimensional sphere function:
    https://www.sfu.ca/~ssurjano/spheref.html
    The global minimum is 0 at (0, ..., 0).

    Note that here we use a network topology where each node has access to the best 
    solution only in its neighbourhood. We also change the network topology over time,
    in accordance with the procedure described in Liu et al. 2016, "Dynamic Small 
    World Network Topology for Particle Swarm Optimization", making this system 
    a network automaton with changing activities and topology.
    
    each node (i.e. particle) has a state with the following:
    - current solution vector x_i
    - best solution vector p_i
    - velocity vector v_i
    """
    n_particles = 20
    timesteps = 500
    dim = 30
    k = 4  # Watts-Strogatz graph k-value
    inertia_weight = 0.729  # w
    cognitive_coefficient = 1  # phi_p
    social_coefficient = 1  # phi_g

    lower_boundary, upper_boundary = -100, 100

    # the initial network is essentially a fully connected network
    network = ntm.topology.watts_strogatz_graph(n=n_particles, k=k, p=0.9)

    initial_conditions = {}
    for node_i in network.nodes:
        x_i = np.random.uniform(low=lower_boundary, high=upper_boundary, size=dim)
        p_i = x_i
        abs_diff_bounds = np.abs(upper_boundary - lower_boundary)
        v_i = np.random.uniform(low=-abs_diff_bounds, high=abs_diff_bounds, size=dim)
        initial_conditions[node_i] = (x_i, p_i, v_i)


    def activity_rule(ctx):
        x_i, p_i, v_i = ctx.current_activity

        # figure out g: the best solution in the node's neighbourhood
        g = None
        for _, p, _ in ctx.neighbourhood_activities:
            if g is None or f(p) < f(g):
                g = p

        r_p = np.random.uniform(0, 1, size=dim)
        r_g = np.random.uniform(0, 1, size=dim)
        scalars = np.array([inertia_weight, cognitive_coefficient, social_coefficient])
        v_i = np.array([
            v_i,
            r_p * (p_i - x_i),
            r_g * (g - x_i)
        ]).T.dot(scalars)

        x_i = x_i + v_i

        if f(x_i) < f(p_i):
            p_i = x_i

        return x_i, p_i, v_i


    def topology_rule(ctx):
        new_p = p_decay(ctx.timestep)
        return ntm.topology.watts_strogatz_graph(n=n_particles, k=k, p=new_p)


    def input(t, activities, net):
        best_soln = None
        for _, p, _ in activities.values():
            if best_soln is None or f(p) < f(best_soln):
                best_soln = p

        print("timestep %s: best solution: %.3f" % (t, f(best_soln)))
        if t == timesteps:
            return None  # terminate the search
        return activities


    ntm.evolve(network, initial_conditions=initial_conditions,
               activity_rule=activity_rule, topology_rule=topology_rule,
               update_order=ntm.UpdateOrder.ACTIVITIES_FIRST, input=input)
