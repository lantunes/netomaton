import netomaton as ntm
from netomaton import TuringMachine, TapeCentricTuringMachine


if __name__ == "__main__":

    # A Turing machine with 7 states for the head, and 7 states for each cell in the tape, for the language
    # L = {a^nb^nc^n | n > 0}. If the evolution of the automaton settles on the head state 'q6', then the string is
    # accepted.

    HEAD = {"q0": 0, "q1": 1, "q2": 2, "q3": 3, "q4": 4, "q5": 5, "q6": 6}
    CELL = {" ": 0, "a": 1, "b": 2, "c": 3, "x": 4, "y": 5, "z": 6}

    rule_table = {
        HEAD['q0']: {
            CELL['a']: [HEAD['q1'], CELL['x'], TuringMachine.RIGHT],
            CELL[' ']: [HEAD['q6'], CELL[' '], TuringMachine.STAY],
            CELL['y']: [HEAD['q4'], CELL['y'], TuringMachine.LEFT],
            CELL['b']: [HEAD['q0'], CELL['b'], TuringMachine.STAY],
            CELL['c']: [HEAD['q0'], CELL['c'], TuringMachine.STAY],
            CELL['x']: [HEAD['q0'], CELL['x'], TuringMachine.STAY],
            CELL['z']: [HEAD['q0'], CELL['z'], TuringMachine.STAY],
        },
        HEAD['q1']: {
            CELL['b']: [HEAD['q2'], CELL['y'], TuringMachine.RIGHT],
            CELL['y']: [HEAD['q1'], CELL['y'], TuringMachine.RIGHT],
            CELL['a']: [HEAD['q1'], CELL['a'], TuringMachine.RIGHT],
            CELL['c']: [HEAD['q1'], CELL['c'], TuringMachine.STAY],
            CELL['x']: [HEAD['q1'], CELL['x'], TuringMachine.STAY],
            CELL['z']: [HEAD['q1'], CELL['z'], TuringMachine.STAY],
            CELL[' ']: [HEAD['q1'], CELL[' '], TuringMachine.STAY],
        },
        HEAD['q2']: {
            CELL['c']: [HEAD['q3'], CELL['z'], TuringMachine.LEFT],
            CELL['z']: [HEAD['q2'], CELL['z'], TuringMachine.RIGHT],
            CELL['b']: [HEAD['q2'], CELL['b'], TuringMachine.RIGHT],
            CELL['a']: [HEAD['q2'], CELL['a'], TuringMachine.STAY],
            CELL['x']: [HEAD['q2'], CELL['x'], TuringMachine.STAY],
            CELL['y']: [HEAD['q2'], CELL['y'], TuringMachine.STAY],
            CELL[' ']: [HEAD['q2'], CELL[' '], TuringMachine.STAY],
        },
        HEAD['q3']: {
            CELL['x']: [HEAD['q0'], CELL['x'], TuringMachine.RIGHT],
            CELL['a']: [HEAD['q3'], CELL['a'], TuringMachine.LEFT],
            CELL['b']: [HEAD['q3'], CELL['b'], TuringMachine.LEFT],
            CELL['z']: [HEAD['q3'], CELL['z'], TuringMachine.LEFT],
            CELL['y']: [HEAD['q3'], CELL['y'], TuringMachine.LEFT],
            CELL['c']: [HEAD['q3'], CELL['c'], TuringMachine.STAY],
            CELL[' ']: [HEAD['q3'], CELL[' '], TuringMachine.STAY]
        },
        HEAD['q4']: {
            CELL[' ']: [HEAD['q5'], CELL[' '], TuringMachine.RIGHT],
            CELL['x']: [HEAD['q4'], CELL['x'], TuringMachine.LEFT],
            CELL['a']: [HEAD['q4'], CELL['a'], TuringMachine.STAY],
            CELL['b']: [HEAD['q4'], CELL['b'], TuringMachine.STAY],
            CELL['c']: [HEAD['q4'], CELL['c'], TuringMachine.STAY],
            CELL['y']: [HEAD['q4'], CELL['y'], TuringMachine.STAY],
            CELL['z']: [HEAD['q4'], CELL['z'], TuringMachine.STAY]
        },
        HEAD['q5']: {
            CELL[' ']: [HEAD['q6'], CELL[' '], TuringMachine.STAY],
            CELL['x']: [HEAD['q5'], CELL['x'], TuringMachine.RIGHT],
            CELL['y']: [HEAD['q5'], CELL['y'], TuringMachine.RIGHT],
            CELL['z']: [HEAD['q5'], CELL['z'], TuringMachine.RIGHT],
            CELL['a']: [HEAD['q5'], CELL['a'], TuringMachine.STAY],
            CELL['b']: [HEAD['q5'], CELL['b'], TuringMachine.STAY],
            CELL['c']: [HEAD['q5'], CELL['c'], TuringMachine.STAY]
        },
        HEAD['q6']: {
            CELL[' ']: [HEAD['q6'], CELL[' '], TuringMachine.STAY],
            CELL['a']: [HEAD['q6'], CELL['a'], TuringMachine.STAY],
            CELL['b']: [HEAD['q6'], CELL['b'], TuringMachine.STAY],
            CELL['c']: [HEAD['q6'], CELL['c'], TuringMachine.STAY],
            CELL['x']: [HEAD['q6'], CELL['x'], TuringMachine.STAY],
            CELL['y']: [HEAD['q6'], CELL['y'], TuringMachine.STAY],
            CELL['z']: [HEAD['q6'], CELL['z'], TuringMachine.STAY]
        }
    }

    tape = "  aabbcc  "

    tm = TapeCentricTuringMachine(num_cells=len(tape), rule_table=rule_table,
                                  initial_head_state=HEAD['q0'], initial_head_position=2)

    initial_conditions = [CELL[t] for t in tape]

    activities, _ = ntm.evolve(initial_conditions, tm.adjacencies, activity_rule=tm.activity_rule, timesteps=61)

    ntm.plot_grid(activities, cell_annotations=tm.head_activities(activities), show_grid=True)
