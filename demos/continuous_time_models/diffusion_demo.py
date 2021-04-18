import netomaton as ntm
import numpy as np


if __name__ == "__main__":
    """
    A model of the 1D Diffusion equation: ∂u/∂t = ν ∂²u/∂x²

    Based on: https://nbviewer.jupyter.org/github/barbagroup/CFDPython/blob/master/lessons/04_Step_3.ipynb
    """
    nx = 41                    # the number of nodes (i.e. the number of points in the grid)
    nt = 99                    # the number of timesteps
    dx = 2 / (nx - 1)          # the distance between any pair of adjacent points
    nu = 0.3                   # the value of viscosity
    sigma = .2                 # Courant number
    dt = sigma * dx ** 2 / nu  # the amount of time each timestep covers

    network = ntm.topology.cellular_automaton(nx)

    initial_conditions = [1.] * 10 + [2.] * 11 + [1.] * 20


    def activity_rule(ctx):
        un_i = ctx.current_activity
        left_label = (ctx.node_label - 1) % nx
        un_i_m1 = ctx.activity_of(left_label)
        right_label = (ctx.node_label + 1) % nx
        un_i_p1 = ctx.activity_of(right_label)
        return un_i + nu * dt / dx ** 2 * (un_i_p1 - 2 * un_i + un_i_m1)


    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=nt)

    ntm.plot_activities(trajectory)

    ntm.animate_plot1D(np.linspace(0, 2, nx), trajectory)
