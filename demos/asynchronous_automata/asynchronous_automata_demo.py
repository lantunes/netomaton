from netomaton import *


if __name__ == '__main__':
    adjacencies = AdjacencyMatrix.cellular_automaton(n=21)

    # implements the rule 60 sequential automaton from the NKS Notes on
    #   Chapter 9, section 10: "Sequential cellular automata"
    #   http://www.wolframscience.com/nks/notes-9-10--sequential-cellular-automata/
    initial_conditions =[0]*10 + [1] + [0]*10

    r = AsynchronousRule(activity_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 60), update_order=range(1, 20))

    activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=19*20,
                                        activity_rule=r.activity_rule)

    # plot every 19th row, including the first, as a cycle is completed every 19 rows
    plot_grid(activities[::19])
