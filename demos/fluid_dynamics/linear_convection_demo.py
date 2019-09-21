import netomaton as ntm
import numpy as np
from matplotlib import pyplot, animation


if __name__ == "__main__":
    """
    A model of the 1D Linear Convection equation: ∂u/∂t + k ∂u/∂x = 0
    
    Based on: https://nbviewer.jupyter.org/github/barbagroup/CFDPython/blob/master/lessons/01_Step_1.ipynb
    """

    nx = 41            # the number of cells (i.e. the number of points in the grid)
    nt = 59            # the number of timesteps
    dt = .025          # the amount of time each timestep covers
    dx = 2 / (nx - 1)  # the distance between any pair of adjacent points
    k = 1              # wavespeed of 1

    adjacencies = ntm.network.cellular_automaton(nx)

    initial_conditions = [1.]*10 + [2.]*11 + [1.]*20

    def activity_rule(n, c, t):
        un_i = n.current_activity
        # the space derivative is handled using the Backward Difference, i.e. the value of the neighbour to the left
        left_index = (c-1) % nx
        un_i_m1 = n.activities[n.neighbour_indices.index(left_index)]
        return un_i - k * dt / dx * (un_i - un_i_m1)


    activities, _ = ntm.evolve(initial_conditions, adjacencies, activity_rule, timesteps=nt)

    ntm.plot_grid(activities)

    ntm.animate(activities, shape=(1, nx))

    fig1 = pyplot.figure()
    line, = pyplot.plot(np.linspace(0, 2, nx), activities[0])
    def update_line(activity):
        line.set_data(np.linspace(0, 2, nx), activity)
        return line,
    line_ani = animation.FuncAnimation(fig1, update_line, frames=activities, blit=True, interval=50)
    pyplot.show()
