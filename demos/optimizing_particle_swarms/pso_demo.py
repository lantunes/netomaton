import netomaton as ntm
import numpy as np


def f(x):
    # the six-hump camel function
    x1, x2 = x
    return (4 - (2.1 * x1 ** 2) + ((x1 ** 4) / 3)) * x1 ** 2 + x1 * x2 + (-4 + (4 * x2 ** 2)) * x2 ** 2


if __name__ == '__main__':
    """
    See: https://en.wikipedia.org/wiki/Particle_swarm_optimization#Algorithm
    
    Here we search for the minimum of the six-hump camel function: 
    https://www.sfu.ca/~ssurjano/camel6.html
    The global minimum is -1.0316 at (0.0898, -0.7126) and (-0.0898, 0.7126).
    
    each node (i.e. particle) has a state with the following:
    - current solution vector x_i
    - best solution vector p_i
    - velocity vector v_i
    """
    n_particles = 10
    timesteps = 30
    g = None  # the best position found by the swarm
    inertia_weight = 0.5  # w
    cognitive_coefficient = 1  # phi_p
    social_coefficient = 1  # phi_g

    upper_boundary = np.array([3, 2])  # b_up
    lower_boundary = np.array([-3, -2])  # b_lo

    # a fully connected network of particles;
    #  in this implementation, the network could also be fully disconnected, but the idea is
    #  that the best global solution is communicated to all particles in the swarm, and the
    #  fully connected network symbolizes this
    network = ntm.topology.complete(n_particles)

    initial_conditions = {}
    for node_i in network.nodes:
        x_i = np.random.uniform(lower_boundary, upper_boundary)
        p_i = x_i
        abs_diff_bounds = np.abs(upper_boundary - lower_boundary)
        v_i = np.random.uniform(-abs_diff_bounds, abs_diff_bounds)
        if g is None or f(p_i) < f(g):
            g = p_i
        initial_conditions[node_i] = (x_i, p_i, v_i)


    def activity_rule(ctx):
        global g
        x_i, p_i, v_i = ctx.current_activity

        r_p = np.random.uniform(0, 1, size=2)
        r_g = np.random.uniform(0, 1, size=2)
        scalars = np.array([inertia_weight, cognitive_coefficient, social_coefficient])
        v_i = np.array([
            v_i,
            r_p * (p_i - x_i),
            r_g * (g - x_i)
        ]).T.dot(scalars)

        x_i = x_i + v_i

        if f(x_i) < f(p_i):
            p_i = x_i

            if f(p_i) < f(g):
                g = p_i

        return x_i, p_i, v_i

    def input(t, activities, net):
        print("timestep %s: best solution: %s (%s)" % (t, g, f(g)))
        if t == timesteps:
            return None  # terminate the search
        return activities

    ntm.evolve(network, initial_conditions=initial_conditions,
               activity_rule=activity_rule, input=input)
