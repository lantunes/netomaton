import netomaton as ntm

"""
A Sierpinski Triangle.

See: https://en.wikipedia.org/wiki/L-system
"""

if __name__ == '__main__':
    system = ntm.SubstitutionSystem(rules={
        "F": "F-G+F+G-F",
        "G": "GG"
    }, constants=["+", "-"], axiom="F-G-G")

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=6)

    t = ntm.Turtle()
    ntm.plot_L_system(state=trajectory[-1], turtle=t, bindings={
        "F": (t.forward, 1),
        "G": (t.forward, 1),
        "+": (t.rotate, -120),
        "-": (t.rotate, 120)
    })
