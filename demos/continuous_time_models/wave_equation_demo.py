import netomaton as ntm
import numpy as np


if __name__ == "__main__":
    """
    Simulates the Wave Equation:
    
    ∂²u/∂t² = ∂²u/∂x²
    
    Reproduces the middle plot of Wolfram's NKS, page 163. 
    
    See: https://www.wolframscience.com/nks/p163--partial-differential-equations/
    """
    nx = 401  # the number of cells (i.e. the number of points in the grid)
    nt = 255  # the number of timesteps
    dx = 0.1  # the distance between any pair of adjacent points
    dt = .05  # the amount of time each timestep covers

    space = np.linspace(20, -20, nx)
    initial_conditions = [np.exp(-x ** 2) for x in space]

    adjacencies = ntm.network.cellular_automaton(nx)

    # TODO perhaps we should provide the option to provide more than just the current activities
    #  n.activities_at(timestep)[cell_index]
    t_m1 = initial_conditions  # the activities at t-1
    def activity_rule(n, c, t):
        un_i = n.current_activity
        left_index = (c - 1) % nx
        un_i_m1 = n.activities[n.neighbour_indices.index(left_index)]
        right_index = (c + 1) % nx
        un_i_p1 = n.activities[n.neighbour_indices.index(right_index)]
        un_m1_i = t_m1[c]  # the activity not at the previous timestep, but the timestep before that
        new_un_i = ((dt**2 * (un_i_p1 - 2*un_i + un_i_m1)) / dx**2) + (2*un_i - un_m1_i)
        t_m1[c] = un_i
        return new_un_i

    activities, _ = ntm.evolve(initial_conditions, adjacencies, activity_rule, timesteps=nt)

    ntm.plot_grid(activities)

    ntm.animate_plot1D(np.linspace(0, 2, nx), activities)
