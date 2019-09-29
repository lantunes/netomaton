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

    subn_system = ntm.SubstitutionSystem(rules, len(initial_conditions))

    activities, connectivities = ntm.evolve(initial_conditions, subn_system.adjacency_matrix,
                                            connectivity_rule=subn_system.connectivity_rule,
                                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(activities)

    ntm.plot_grid(padded, show_grid=True)
