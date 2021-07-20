import netomaton as ntm


if __name__ == '__main__':
    dim = (75, 75)
    rule = ntm.LangtonsLoop(dim=dim)

    initial_conditions = rule.init_loops(1, [40], [25])

    trajectory = ntm.evolve(initial_conditions=initial_conditions,
                            network=rule.network, timesteps=500,
                            activity_rule=rule.activity_rule)

    ntm.animate_activities(trajectory, shape=dim)
