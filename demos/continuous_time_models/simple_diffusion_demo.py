import numpy as np
import netomaton as ntm

if __name__ == "__main__":
    """
    Simulates the 1D Diffusion Equation (also known as the heat equation):

    ∂u/∂t = α ∂²u/∂x²

    Each of the 120 nodes represents a body that can contain some amount of heat. Reproduces the plot at the top of 
    Wolfram's NKS, page 163. 

    See: https://www.wolframscience.com/nks/p163--partial-differential-equations/
    See: http://hplgit.github.io/num-methods-for-PDEs/doc/pub/diffu/sphinx/._main_diffu001.html
    """

    space = np.linspace(25, -25, 120)
    initial_conditions = [np.exp(-x ** 2) for x in space]

    network = ntm.topology.cellular_automaton(120)

    a = 0.25
    dt = .5
    dx = .5
    F = a * dt / dx ** 2

    def activity_rule(ctx):
        current = ctx.current_activity
        left = ctx.neighbourhood_activities[0]
        right = ctx.neighbourhood_activities[2]
        return current + F * (right - 2 * current + left)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                               activity_rule=activity_rule, timesteps=75)

    ntm.plot_activities(trajectory)
