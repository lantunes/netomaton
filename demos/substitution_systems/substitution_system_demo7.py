import netomaton as ntm

if __name__ == "__main__":

    system = ntm.SubstitutionSystem(rules={
        "111": "22",
        "112": "121",
        "121": "11",
        "122": "",
        "211": "212",
        "212": "1",
        "221": "22",
        "222": "211",
    }, axiom=[2, 1, 1, 2, 1, 2])

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=5)

    padded = system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)
