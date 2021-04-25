import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 82 (left)
    system = ntm.SubstitutionSystem(rules={
        "2": "21",
        "1": "12"
    }, axiom=[2])

    trajectory = ntm.evolve(network=system.network,
                            initial_conditions=system.initial_conditions,
                            activity_rule=system.activity_rule, timesteps=6)

    padded = system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)
