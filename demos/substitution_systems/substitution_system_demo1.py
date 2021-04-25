import netomaton as ntm

if __name__ == "__main__":

    # NKS p. 82 (left)
    rules = {
        "2": "21",
        "1": "12"
    }
    initial_conditions = [2]
    timesteps = 6

    subn_system = ntm.SubstitutionSystem(rules=rules, n=len(initial_conditions), dtype=int)

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=subn_system.network,
                            activity_rule=subn_system.activity_rule, timesteps=timesteps)

    padded = subn_system.pad(trajectory)

    ntm.plot_grid(padded, show_grid=True)
