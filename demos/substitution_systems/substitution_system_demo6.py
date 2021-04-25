import netomaton as ntm

if __name__ == "__main__":

    system = ntm.SubstitutionSystem(rules={
        "22": "22",
        "21": "1",
        "12": "21",
        "11": ""
    }, axiom=[1, 2, 2, 1])

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=4)

    padded = system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)
