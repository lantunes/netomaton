import netomaton as ntm

"""
A Fractal Plant.

See: https://en.wikipedia.org/wiki/L-system
"""

if __name__ == '__main__':
    system = ntm.SubstitutionSystem(rules={
        "X": "F+[[X]-X]-F[-FX]+X",
        "F": "FF"
    }, constants=["+", "-", "[", "]"], axiom="X")

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=6)

    t = ntm.Turtle(start_orientation=25)
    ntm.animate_L_system(state=trajectory[-1], turtle=t, bindings={
        "F": (t.forward, 1),
        "X": [],
        "+": (t.rotate, -25),
        "-": (t.rotate, 25),
        "[": t.push,
        "]": t.pop,
    }, repeat=True, interval=1)
