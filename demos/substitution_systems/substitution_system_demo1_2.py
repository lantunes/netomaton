import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 82 (left)
    rules = {
        "2": "21",
        "1": "12"
    }
    initial_conditions = [2]
    timesteps = 6

    subn_system = ntm.SubstitutionSystem_2(rules, len(initial_conditions))

    activities, connectivities = ntm.evolve_2(initial_conditions=initial_conditions,
                                              topology=subn_system.connectivity_map,
                                              activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(activities)

    ntm.plot_grid(padded, show_grid=True)
