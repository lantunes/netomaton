import netomaton as ntm


if __name__ == '__main__':
    adjacency_matrix = ntm.topology.adjacency.cellular_automaton(n=21)

    # implements the rule 60 sequential automaton from the NKS Notes on
    #   Chapter 9, section 10: "Sequential cellular automata"
    #   http://www.wolframscience.com/nks/notes-9-10--sequential-cellular-automata/
    initial_conditions =[0]*10 + [1] + [0]*10

    r = ntm.AsynchronousRule_2(activity_rule=ntm.rules.nks_ca_rule_2(60),
                               update_order=range(1, 20))

    activities, adjacencies = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                           timesteps=19*20, activity_rule=r)

    # plot every 19th row, including the first, as a cycle is completed every 19 rows
    ntm.plot_grid(activities[::19])
