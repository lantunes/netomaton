import netomaton as ntm


if __name__ == '__main__':
    adjacencies = ntm.network.cellular_automaton(n=21)

    # implements the rule 60 sequential automaton from the NKS Notes on
    #   Chapter 9, section 10: "Sequential cellular automata"
    #   http://www.wolframscience.com/nks/notes-9-10--sequential-cellular-automata/
    initial_conditions =[0]*10 + [1] + [0]*10

    r = ntm.AsynchronousRule(activity_rule=lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 60),
                             update_order=range(1, 20))

    activities, connectivities = ntm.evolve(initial_conditions, adjacencies, timesteps=19*20,
                                            activity_rule=r.activity_rule)

    # plot every 19th row, including the first, as a cycle is completed every 19 rows
    ntm.plot_grid(activities[::19])
