import netomaton as ntm

"""
A Koch Curve.

See: https://en.wikipedia.org/wiki/L-system
"""

if __name__ == '__main__':
    system = ntm.SubstitutionSystem(n=1, rules={
        "F": "F+F-F-F+F"
    }, constants=["+", "-"])

    initial_conditions = ["F"]

    trajectory = ntm.evolve(network=system.network, initial_conditions=initial_conditions,
                            activity_rule=system.activity_rule, timesteps=4)

    t = ntm.Turtle(start_orientation=90)
    ntm.plot_L_system(state=trajectory[-1], turtle=t, bindings={
        "F": (t.forward, 1),
        "+": (t.rotate, -90),
        "-": (t.rotate, 90)
    })