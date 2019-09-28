import netomaton as ntm
import numpy as np


if __name__ == "__main__":
    """
    A model of Burger's Equation: ∂u/∂t + u ∂u/∂x = ν ∂²u/∂x²
    
    Based on: https://nbviewer.jupyter.org/github/barbagroup/CFDPython/blob/master/lessons/05_Step_4.ipynb
    """

    nx = 101                   # the number of cells (i.e. the number of points in the grid)
    nt = 500                   # the number of timesteps
    dx = 2 * np.pi / (nx - 1)  # the distance between any pair of adjacent points
    nu = .07                   # the value of viscosity
    dt = dx * nu               # the amount of time each timestep covers

    adjacencies = ntm.network.cellular_automaton(nx)

    # Sawtooth initial conditions
    initial_conditions = [4.        ,  4.06283185,  4.12566371,  4.18849556,  4.25132741,
                          4.31415927,  4.37699112,  4.43982297,  4.50265482,  4.56548668,
                          4.62831853,  4.69115038,  4.75398224,  4.81681409,  4.87964594,
                          4.9424778 ,  5.00530965,  5.0681415 ,  5.13097336,  5.19380521,
                          5.25663706,  5.31946891,  5.38230077,  5.44513262,  5.50796447,
                          5.57079633,  5.63362818,  5.69646003,  5.75929189,  5.82212374,
                          5.88495559,  5.94778745,  6.0106193 ,  6.07345115,  6.136283  ,
                          6.19911486,  6.26194671,  6.32477856,  6.38761042,  6.45044227,
                          6.51327412,  6.57610598,  6.63893783,  6.70176967,  6.76460125,
                          6.82742866,  6.89018589,  6.95176632,  6.99367964,  6.72527549,
                          4.        ,  1.27472451,  1.00632036,  1.04823368,  1.10981411,
                          1.17257134,  1.23539875,  1.29823033,  1.36106217,  1.42389402,
                          1.48672588,  1.54955773,  1.61238958,  1.67522144,  1.73805329,
                          1.80088514,  1.863717  ,  1.92654885,  1.9893807 ,  2.05221255,
                          2.11504441,  2.17787626,  2.24070811,  2.30353997,  2.36637182,
                          2.42920367,  2.49203553,  2.55486738,  2.61769923,  2.68053109,
                          2.74336294,  2.80619479,  2.86902664,  2.9318585 ,  2.99469035,
                          3.0575222 ,  3.12035406,  3.18318591,  3.24601776,  3.30884962,
                          3.37168147,  3.43451332,  3.49734518,  3.56017703,  3.62300888,
                          3.68584073,  3.74867259,  3.81150444,  3.87433629,  3.93716815,  4.]


    def activity_rule(ctx):
        un_i = ctx.current_activity
        left_index = (ctx.cell_index - 1) % nx
        un_i_m1 = ctx.activity_of(left_index)
        right_index = (ctx.cell_index + 1) % nx
        un_i_p1 = ctx.activity_of(right_index)
        return un_i - un_i * dt/dx * (un_i - un_i_m1) + nu * dt/dx**2 * (un_i_p1 - 2*un_i + un_i_m1)


    activities, _ = ntm.evolve(initial_conditions, adjacencies, activity_rule, timesteps=nt)

    ntm.plot_grid(activities)

    ntm.animate_plot1D(np.linspace(0, 2, nx), activities)
