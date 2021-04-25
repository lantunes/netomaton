import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 87 (b)
    system = ntm.SubstitutionSystem(rules={
        "33": "3",
        "32": "12",
        "31": "1",
        "23": "",
        "22": "",
        "21": "3",
        "13": "1",
        "12": "12",
        "11": "3"
    }, axiom=[1, 2, 3, 2])

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=101)

    padded = system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)
