import netomaton as ntm

if __name__ == "__main__":

    rules = {
        "2": "212",
        "1": "121"
    }
    initial_conditions = [2]
    timesteps = 4

    subn_system = ntm.SubstitutionSystem(rules, len(initial_conditions))

    activities, connectivities = ntm.evolve(initial_conditions, subn_system.adjacency_matrix,
                                            connectivity_rule=subn_system.connectivity_rule,
                                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(activities)

    ntm.plot_grid(padded, show_grid=True)
