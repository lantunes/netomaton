import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 86
    rules = {
        "22": "22",
        "21": "1",
        "12": "21",
        "11": ""
    }
    initial_conditions = [1, 2, 2, 1]
    timesteps = 13

    subn_system = ntm.SubstitutionSystem(rules, len(initial_conditions))

    activities, connectivities = ntm.evolve(initial_conditions=initial_conditions,
                                            topology=subn_system.connectivity_map,
                                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(activities)
    ntm.plot_grid(padded, show_grid=True)

    ntm.animate_connectivity_map(connectivities, interval=250)
