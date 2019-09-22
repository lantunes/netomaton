import netomaton as ntm
import numpy as np


if __name__ == "__main__":
    """
    A model of the 1D Diffusion equation: ∂u/∂t = ν ∂²u/∂x²

    Based on: https://nbviewer.jupyter.org/github/barbagroup/CFDPython/blob/master/lessons/04_Step_3.ipynb
    """
    nx = 41                    # the number of cells (i.e. the number of points in the grid)
    nt = 99                    # the number of timesteps
    dx = 2 / (nx - 1)          # the distance between any pair of adjacent points
    nu = 0.3                   # the value of viscosity
    sigma = .2                 # Courant number
    dt = sigma * dx ** 2 / nu  # the amount of time each timestep covers

    adjacencies = ntm.network.cellular_automaton(nx)

    initial_conditions = [1.] * 10 + [2.] * 11 + [1.] * 20


    def activity_rule(n, c, t):
        un_i = n.current_activity
        left_index = (c - 1) % nx
        un_i_m1 = n.activities[n.neighbour_indices.index(left_index)]
        right_index = (c + 1) % nx
        un_i_p1 = n.activities[n.neighbour_indices.index(right_index)]
        return un_i + nu * dt / dx**2 * (un_i_p1 - 2 * un_i + un_i_m1)


    activities, _ = ntm.evolve(initial_conditions, adjacencies, activity_rule, timesteps=nt)

    ntm.plot_grid(activities)

    ntm.animate_plot1D(np.linspace(0, 2, nx), activities)
