import netomaton as ntm

if __name__ == "__main__":
    """
    In this single-node Network Automaton, the node's state consists of two continuous values, which represent 
    position and velocity. The state changes according to the following equations of motion:

    dx/dt = v
    dv/dt = −k⁄m x − b⁄m v

    where x is position, v is velocity, k is stiffness, b is damping, m is mass, t is time

    This makes the node's state change as if it had the mechanics of a single spring. Since a Network Automaton exists
    in discrete time, the state will be updated with difference equations, using the Euler method. 
    For k = 3.0, m = 0.5, b = 0.0:

    dx/dt = v
    dv/dt = −6 x

    The difference equations are:

    x[n+1] = x[n] + Δt*v[n]
    v[n+1] = v[n] + Δt*(−6x[n])
    """

    network = ntm.topology.from_adjacency_matrix([[1]])

    dt = 0.025000

    def activity_rule(ctx):
        x_n, v_n = ctx.current_activity
        x_new = x_n + (dt * v_n)
        v_new = v_n + (dt * (-6 * x_new))
        return x_new, v_new

    initial_conditions = [(-2.00000, 0.00000)]

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=1000)

    activities = ntm.get_activities_over_time_as_list(trajectory)

    # plot the position and velocity as a function of time
    positions = [a[0][0] for a in activities]
    velocities = [a[0][1] for a in activities]
    ntm.plot1D(x=[i for i in range(1000)],
               y=[positions, velocities],
               color=["blue", "orange"],
               xlabel="t", ylabel=["x(t)", "v(t)"],
               ylim=[(-6, 6), (-6, 6)], twinx=True)
