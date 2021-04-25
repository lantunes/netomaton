import netomaton as ntm

"""
A Fractal Tree.

See: https://en.wikipedia.org/wiki/L-system
"""

if __name__ == '__main__':
    system = ntm.SubstitutionSystem(rules={
        "1": "11",
        "0": "1[0]0"
    }, constants=["[", "]"], axiom="0")

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=7)

    t = ntm.Turtle()
    ntm.plot_L_system(state=trajectory[-1], turtle=t, bindings={
        "1": t.forward,
        "0": t.forward,
        "[": [t.push, (t.rotate, -45)],
        "]": [t.pop, (t.rotate, 45)]
    })
