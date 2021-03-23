import netomaton as ntm

if __name__ == "__main__":

    # rules = {
    #     "2": "212",
    #     "1": "121"
    # }
    # initial_conditions = [2]

    rules = {
        "22": "22",
        "21": "1",
        "12": "21",
        "11": ""
    }
    initial_conditions = [1, 2, 2, 1]

    timesteps = 4

    subn_system = ntm.SubstitutionSystem2(rules, len(initial_conditions))

    activities, connectivities = ntm.evolve_2(initial_conditions=initial_conditions,
                                              topology=subn_system.connectivity_map,
                                              activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(activities)

    ntm.plot_grid(padded, show_grid=True)
