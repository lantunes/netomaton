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

    subn_system = ntm.SubstitutionSystem(rules=rules, n=len(initial_conditions), dtype=int)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=subn_system.network,
                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)
