import netomaton as ntm
from netomaton import TuringMachine_2, HeadCentricTuringMachine_2


if __name__ == "__main__":

    # A Turing machine with 2 states for the head, and 5 states for each cell in the tape.
    # This is the simple universal Turing machine described in Wolfram's New Kind of Science, which emulates
    # ECA Rule 110 (also known to be universal).
    # See: https://www.wolframscience.com/nks/p707--universality-in-turing-machines-and-other-systems/

    HEAD = {"up": 1, "down": 2}
    CELL = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}

    rule_table = {
        HEAD['up']: {
            CELL['a']: [HEAD['up'], CELL['b'], TuringMachine_2.LEFT],
            CELL['b']: [HEAD['up'], CELL['a'], TuringMachine_2.RIGHT],
            CELL['c']: [HEAD['up'], CELL['a'], TuringMachine_2.RIGHT],
            CELL['d']: [HEAD['down'], CELL['e'], TuringMachine_2.RIGHT],
            CELL['e']: [HEAD['down'], CELL['d'], TuringMachine_2.LEFT]
        },
        HEAD['down']: {
            CELL['a']: [HEAD['up'], CELL['d'], TuringMachine_2.LEFT],
            CELL['b']: [HEAD['up'], CELL['a'], TuringMachine_2.RIGHT],
            CELL['c']: [HEAD['up'], CELL['e'], TuringMachine_2.RIGHT],
            CELL['d']: [HEAD['down'], CELL['e'], TuringMachine_2.RIGHT],
            CELL['e']: [HEAD['down'], CELL['c'], TuringMachine_2.LEFT]
        }
    }

    tape = "bbbbbbaeaaaaaaa"

    tm = HeadCentricTuringMachine_2(tape=[CELL[t] for t in tape], rule_table=rule_table,
                                    initial_head_state=HEAD['up'], initial_head_position=8, max_timesteps=58)

    activities, _ = ntm.evolve_2(initial_conditions=tm.initial_conditions, topology=tm.adjacency_matrix,
                                 activity_rule=tm.activity_rule, input=tm.input_function)

    tape_history, head_activities = tm.activities_for_plotting(activities)

    ntm.plot_grid(tape_history, node_annotations=head_activities, show_grid=True)

    # The following is a longer evolution, to show that ECA Rule 110 is emulated;
    #  it will start when the plot rendered above is closed.

    tape = "b"*50 + "ae" + "a"*51

    tm = HeadCentricTuringMachine_2(tape=[CELL[t] for t in tape], rule_table=rule_table,
                                    initial_head_state=HEAD['up'], initial_head_position=52, max_timesteps=5000)

    activities, _ = ntm.evolve_2(initial_conditions=tm.initial_conditions, topology=tm.adjacency_matrix,
                                 activity_rule=tm.activity_rule, input=tm.input_function)

    tape_history, head_activities = tm.activities_for_plotting(activities)

    # we'll only keep the steps where the head has moved further to the right than ever before...
    compressed_activities = []
    compressed_head_activities = []
    furthest_head_idx = 0
    for i, row in enumerate(head_activities):
        try:
            head_idx = row.index(str(HEAD['up']))
        except ValueError:
            head_idx = row.index(str(HEAD['down']))
        if head_idx > furthest_head_idx:
            compressed_activities.append(tape_history[i])
            compressed_head_activities.append(row)
            furthest_head_idx = head_idx

    ntm.plot_grid(compressed_activities, node_annotations=compressed_head_activities, show_grid=True)
