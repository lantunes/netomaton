import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 87 (b)
    rules = {
        "33": "3",
        "32": "12",
        "31": "1",
        "23": "",
        "22": "",
        "21": "3",
        "13": "1",
        "12": "12",
        "11": "3"
    }
    initial_conditions = [1, 2, 3, 2]
    timesteps = 101

    subn_system = ntm.SubstitutionSystem_2(rules, len(initial_conditions))

    activities, connectivities = ntm.evolve_2(initial_conditions=initial_conditions,
                                              topology=subn_system.connectivity_map,
                                              activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(activities)

    ntm.plot_grid(padded, show_grid=True)
