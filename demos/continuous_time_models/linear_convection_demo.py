import netomaton as ntm
import numpy as np

if __name__ == "__main__":
    """
    A model of the 1D Linear Convection equation: ∂u/∂t + k ∂u/∂x = 0

    Based on: https://nbviewer.jupyter.org/github/barbagroup/CFDPython/blob/master/lessons/01_Step_1.ipynb
    """

    nx = 41  # the number of nodes (i.e. the number of points in the grid)
    nt = 59  # the number of timesteps
    dt = .025  # the amount of time each timestep covers
    dx = 2 / (nx - 1)  # the distance between any pair of adjacent points
    k = 1  # wavespeed of 1

    network = ntm.topology.cellular_automaton(nx)

    initial_conditions = [1.] * 10 + [2.] * 11 + [1.] * 20

    def activity_rule(ctx):
        un_i = ctx.current_activity
        # the space derivative is handled using the Backward Difference, i.e. the value of the neighbour to the left
        left_label = (ctx.node_label - 1) % nx
        un_i_m1 = ctx.activity_of(left_label)
        return un_i - k * dt / dx * (un_i - un_i_m1)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=activity_rule, timesteps=nt)

    ntm.plot_activities(trajectory)

    ntm.animate_plot1D(np.linspace(0, 2, nx), trajectory)
