import netomaton as ntm
from netomaton import TuringMachine_2, HeadCentricTuringMachine_2


if __name__ == "__main__":

    # A Turing machine with 7 states for the head, and 7 states for each cell in the tape, for the language
    # L = {a^nb^nc^n | n > 0}. If the evolution of the automaton settles on the head state 'q6', then the string is
    # accepted.

    HEAD = {"q0": 0, "q1": 1, "q2": 2, "q3": 3, "q4": 4, "q5": 5, "q6": 6}
    CELL = {" ": 0, "a": 1, "b": 2, "c": 3, "x": 4, "y": 5, "z": 6}

    rule_table = {
        HEAD['q0']: {
            CELL['a']: [HEAD['q1'], CELL['x'], TuringMachine_2.RIGHT],
            CELL[' ']: [HEAD['q6'], CELL[' '], TuringMachine_2.STAY],
            CELL['y']: [HEAD['q4'], CELL['y'], TuringMachine_2.LEFT],
            CELL['b']: [HEAD['q0'], CELL['b'], TuringMachine_2.STAY],
            CELL['c']: [HEAD['q0'], CELL['c'], TuringMachine_2.STAY],
            CELL['x']: [HEAD['q0'], CELL['x'], TuringMachine_2.STAY],
            CELL['z']: [HEAD['q0'], CELL['z'], TuringMachine_2.STAY],
        },
        HEAD['q1']: {
            CELL['b']: [HEAD['q2'], CELL['y'], TuringMachine_2.RIGHT],
            CELL['y']: [HEAD['q1'], CELL['y'], TuringMachine_2.RIGHT],
            CELL['a']: [HEAD['q1'], CELL['a'], TuringMachine_2.RIGHT],
            CELL['c']: [HEAD['q1'], CELL['c'], TuringMachine_2.STAY],
            CELL['x']: [HEAD['q1'], CELL['x'], TuringMachine_2.STAY],
            CELL['z']: [HEAD['q1'], CELL['z'], TuringMachine_2.STAY],
            CELL[' ']: [HEAD['q1'], CELL[' '], TuringMachine_2.STAY],
        },
        HEAD['q2']: {
            CELL['c']: [HEAD['q3'], CELL['z'], TuringMachine_2.LEFT],
            CELL['z']: [HEAD['q2'], CELL['z'], TuringMachine_2.RIGHT],
            CELL['b']: [HEAD['q2'], CELL['b'], TuringMachine_2.RIGHT],
            CELL['a']: [HEAD['q2'], CELL['a'], TuringMachine_2.STAY],
            CELL['x']: [HEAD['q2'], CELL['x'], TuringMachine_2.STAY],
            CELL['y']: [HEAD['q2'], CELL['y'], TuringMachine_2.STAY],
            CELL[' ']: [HEAD['q2'], CELL[' '], TuringMachine_2.STAY],
        },
        HEAD['q3']: {
            CELL['x']: [HEAD['q0'], CELL['x'], TuringMachine_2.RIGHT],
            CELL['a']: [HEAD['q3'], CELL['a'], TuringMachine_2.LEFT],
            CELL['b']: [HEAD['q3'], CELL['b'], TuringMachine_2.LEFT],
            CELL['z']: [HEAD['q3'], CELL['z'], TuringMachine_2.LEFT],
            CELL['y']: [HEAD['q3'], CELL['y'], TuringMachine_2.LEFT],
            CELL['c']: [HEAD['q3'], CELL['c'], TuringMachine_2.STAY],
            CELL[' ']: [HEAD['q3'], CELL[' '], TuringMachine_2.STAY]
        },
        HEAD['q4']: {
            CELL[' ']: [HEAD['q5'], CELL[' '], TuringMachine_2.RIGHT],
            CELL['x']: [HEAD['q4'], CELL['x'], TuringMachine_2.LEFT],
            CELL['a']: [HEAD['q4'], CELL['a'], TuringMachine_2.STAY],
            CELL['b']: [HEAD['q4'], CELL['b'], TuringMachine_2.STAY],
            CELL['c']: [HEAD['q4'], CELL['c'], TuringMachine_2.STAY],
            CELL['y']: [HEAD['q4'], CELL['y'], TuringMachine_2.STAY],
            CELL['z']: [HEAD['q4'], CELL['z'], TuringMachine_2.STAY]
        },
        HEAD['q5']: {
            CELL[' ']: [HEAD['q6'], CELL[' '], TuringMachine_2.STAY],
            CELL['x']: [HEAD['q5'], CELL['x'], TuringMachine_2.RIGHT],
            CELL['y']: [HEAD['q5'], CELL['y'], TuringMachine_2.RIGHT],
            CELL['z']: [HEAD['q5'], CELL['z'], TuringMachine_2.RIGHT],
            CELL['a']: [HEAD['q5'], CELL['a'], TuringMachine_2.STAY],
            CELL['b']: [HEAD['q5'], CELL['b'], TuringMachine_2.STAY],
            CELL['c']: [HEAD['q5'], CELL['c'], TuringMachine_2.STAY]
        },
        HEAD['q6']: {
            CELL[' ']: [HEAD['q6'], CELL[' '], TuringMachine_2.STAY],
            CELL['a']: [HEAD['q6'], CELL['a'], TuringMachine_2.STAY],
            CELL['b']: [HEAD['q6'], CELL['b'], TuringMachine_2.STAY],
            CELL['c']: [HEAD['q6'], CELL['c'], TuringMachine_2.STAY],
            CELL['x']: [HEAD['q6'], CELL['x'], TuringMachine_2.STAY],
            CELL['y']: [HEAD['q6'], CELL['y'], TuringMachine_2.STAY],
            CELL['z']: [HEAD['q6'], CELL['z'], TuringMachine_2.STAY]
        }
    }

    tape = "  aabbcc  "

    tm = HeadCentricTuringMachine_2(tape=[CELL[t] for t in tape], rule_table=rule_table,
                                    initial_head_state=HEAD['q0'], initial_head_position=2,
                                    terminating_state=HEAD['q6'], max_timesteps=50)

    activities, _ = ntm.evolve_2(initial_conditions=tm.initial_conditions, topology=tm.adjacency_matrix,
                                 activity_rule=tm.activity_rule, input=tm.input_function)

    tape_history, head_activities = tm.activities_for_plotting(activities)

    ntm.plot_grid(tape_history, node_annotations=head_activities, show_grid=True)
