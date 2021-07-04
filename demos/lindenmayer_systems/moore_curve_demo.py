import netomaton as ntm


"""
A Moore space-filling curve.

See: https://en.wikipedia.org/wiki/Moore_curve
"""

if __name__ == '__main__':
    system = ntm.SubstitutionSystem(rules={
        "L": "-RF+LFL+FR-",
        "R": "+LF-RFR-FL+"
    }, constants=["F", "+", "-"], axiom="LFL+F+LFL")

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=5)

    t = ntm.Turtle()
    ntm.plot_L_system(state=trajectory[-1], turtle=t, bindings={
        "F": t.forward,
        "R": [],
        "L": [],
        "+": (t.rotate, 90),
        "-": (t.rotate, -90)
    })
