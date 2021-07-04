import netomaton as ntm


if __name__ == '__main__':

    network = ntm.topology.cellular_automaton(n=200)

    initial_conditions = [0]*100 + [1] + [0]*99

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                            activity_rule=ntm.rules.totalistic_ca(k=3, rule=777), timesteps=100)

    ntm.plot_activities(trajectory)
