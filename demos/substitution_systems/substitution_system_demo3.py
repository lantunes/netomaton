import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 86
    system = ntm.SubstitutionSystem(rules={
        "22": "22",
        "21": "1",
        "12": "21",
        "11": ""
    }, axiom=[1, 2, 2, 1])

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=13)

    padded = system.pad(trajectory)
    ntm.plot_grid(padded, show_grid=True)

    ntm.animate_network(trajectory, interval=250)
