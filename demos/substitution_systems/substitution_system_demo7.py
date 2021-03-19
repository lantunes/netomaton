import netomaton as ntm

if __name__ == "__main__":

    rules = {
        "111": "22",
        "112": "121",
        "121": "11",
        "122": "",
        "211": "212",
        "212": "1",
        "221": "22",
        "222": "211",
    }
    initial_conditions = [2, 1, 1, 2, 1, 2]
    timesteps = 4

    subn_system = ntm.SubstitutionSystem(rules, len(initial_conditions))

    activities, connectivities = ntm.evolve(initial_conditions, subn_system.adjacency_matrix,
                                            connectivity_rule=subn_system.connectivity_rule,
                                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(activities)

    ntm.plot_grid(padded, show_grid=True)
