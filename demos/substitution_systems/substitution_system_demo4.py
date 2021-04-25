import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 87 (a)
    rules = {
        "33": "1",
        "32": "1",
        "31": "3",
        "23": "11",
        "22": "12",
        "21": "22",
        "13": "3",
        "12": "3",
        "11": "1"
    }
    initial_conditions = [1, 2, 2, 1]
    timesteps = 101

    subn_system = ntm.SubstitutionSystem(rules=rules, n=len(initial_conditions), dtype=int)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=subn_system.network,
                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)

    ntm.vis.show_network(trajectory[timesteps-1].network)
