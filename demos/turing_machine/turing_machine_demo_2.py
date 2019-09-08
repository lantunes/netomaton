import netomaton as ntm
from netomaton import TuringMachine, TapeCentricTuringMachine


if __name__ == "__main__":

    # A Turing machine with two possible states for the head, and two possible states for each cell in the tape.
    # A reproduction of the Turing machine given on page 79 (figure (b)) of NKS
    #   (https://www.wolframscience.com/nks/p79--turing-machines/)

    HEAD = {"up": 1, "down": 2}
    CELL = {"on": 1, "off": 0}

    rule_table = {
        HEAD['up']: {
            CELL['on']: [HEAD['up'], CELL['off'], TuringMachine.RIGHT],
            CELL['off']: [HEAD['down'], CELL['on'], TuringMachine.RIGHT]
        },
        HEAD['down']: {
            CELL['on']: [HEAD['up'], CELL['on'], TuringMachine.LEFT],
            CELL['off']: [HEAD['down'], CELL['on'], TuringMachine.LEFT]
        }
    }

    tm = TapeCentricTuringMachine(num_cells=21, rule_table=rule_table,
                                  initial_head_state=HEAD['up'], initial_head_position=3)

    initial_conditions = [0] * 21

    activities, _ = ntm.evolve(initial_conditions, tm.adjacencies, activity_rule=tm.activity_rule, timesteps=61)

    ntm.plot_grid(activities, cell_annotations=tm.head_activities(activities), show_grid=True)
