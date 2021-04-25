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
    timesteps = 5

    subn_system = ntm.SubstitutionSystem(rules=rules, n=len(initial_conditions), dtype=int)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=subn_system.network,
                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)
