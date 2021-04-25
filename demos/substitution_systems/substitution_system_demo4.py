import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 87 (a)
    system = ntm.SubstitutionSystem(rules={
        "33": "1",
        "32": "1",
        "31": "3",
        "23": "11",
        "22": "12",
        "21": "22",
        "13": "3",
        "12": "3",
        "11": "1"
    }, axiom=[1, 2, 2, 1])

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=101)

    padded = system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)

    ntm.vis.show_network(trajectory[-1].network)
