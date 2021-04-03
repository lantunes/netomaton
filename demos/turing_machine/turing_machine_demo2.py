import netomaton as ntm
from netomaton import TuringMachine_2, TapeCentricTuringMachine_2


if __name__ == "__main__":

    # A Turing machine with two possible states for the head, and two possible states for each cell in the tape.
    # A reproduction of the Turing machine given on page 79 (figure (b)) of Wolfram's New Kind of Science.
    # See: https://www.wolframscience.com/nks/p79--turing-machines/

    HEAD = {"up": 1, "down": 2}
    CELL = {"on": 1, "off": 0}

    rule_table = {
        HEAD['up']: {
            CELL['on']: [HEAD['up'], CELL['off'], TuringMachine_2.RIGHT],
            CELL['off']: [HEAD['down'], CELL['on'], TuringMachine_2.RIGHT]
        },
        HEAD['down']: {
            CELL['on']: [HEAD['up'], CELL['on'], TuringMachine_2.LEFT],
            CELL['off']: [HEAD['down'], CELL['on'], TuringMachine_2.LEFT]
        }
    }

    tm = TapeCentricTuringMachine_2(n=21, rule_table=rule_table,
                                    initial_head_state=HEAD['up'], initial_head_position=3)

    initial_conditions = [0] * 21

    activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=tm.adjacency_matrix,
                                 activity_rule=tm.activity_rule, timesteps=61)

    ntm.plot_grid(activities, node_annotations=tm.head_activities(activities), show_grid=True)
