import netomaton as ntm


"""
A Moore space-filling curve.

See: https://en.wikipedia.org/wiki/Moore_curve
"""

if __name__ == '__main__':
    system = ntm.SubstitutionSystem(n=9, rules={
        "L": "-RF+LFL+FR-",
        "R": "+LF-RFR-FL+"
    }, constants=["F", "+", "-"])

    initial_conditions = [s for s in "LFL+F+LFL"]

    trajectory = ntm.evolve(network=system.network, initial_conditions=initial_conditions,
                            activity_rule=system.activity_rule, timesteps=5)

    t = ntm.Turtle()
    ntm.plot_L_system(state=trajectory[-1], turtle=t, bindings={
        "F": (t.forward, 1),
        "R": [],
        "L": [],
        "+": (t.rotate, 90),
        "-": (t.rotate, -90)
    })
