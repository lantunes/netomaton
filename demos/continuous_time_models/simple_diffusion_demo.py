import numpy as np
import netomaton as ntm


if __name__ == "__main__":
    """
    Simulates the 1D Diffusion Equation (also known as the heat equation):
    
    ∂u/∂t = α ∂^2u/∂x^2
    
    Each of the 120 cells represents a body that can contain some amount of heat. Reproduces the plot at the top of 
    Wolfram's NKS, page 163. 
    
    See: https://www.wolframscience.com/nks/p163--partial-differential-equations/
    See: http://hplgit.github.io/num-methods-for-PDEs/doc/pub/diffu/sphinx/._main_diffu001.html
    """

    space = np.linspace(25, -25, 120)
    initial_conditions = [np.exp(-x ** 2) for x in space]

    adjacencies = ntm.network.cellular_automaton(120)

    a = 0.25
    dt = .5
    dx = .5
    F = a * dt / dx ** 2


    def activity_rule(n, c, t):
        current = n.current_activity
        left = n.activities[0]
        right = n.activities[2]
        return current + F * (right - 2 * current + left)


    activities, _ = ntm.evolve(initial_conditions, adjacencies, activity_rule, timesteps=75)

    ntm.plot_grid(activities)
