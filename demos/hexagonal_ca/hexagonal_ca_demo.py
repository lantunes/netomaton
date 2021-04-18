import netomaton as ntm

if __name__ == '__main__':
    network = ntm.topology.cellular_automaton2d(60, 60, r=1, neighbourhood="Hex")

    initial_conditions = ntm.init_simple2d(60, 60)

    def activity_rule(ctx):
        return 1 if sum(ctx.neighbourhood_activities) == 1 else ctx.current_activity

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=31,
                            activity_rule=activity_rule)

    ntm.animate_hex(trajectory, shape=(60, 60), interval=150)
