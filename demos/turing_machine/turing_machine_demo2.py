import netomaton as ntm
from netomaton import TuringMachine, TapeCentricTuringMachine


if __name__ == "__main__":

    # A Turing machine with two possible states for the head, and two possible states for each cell in the tape.
    # A reproduction of the Turing machine given on page 79 (figure (b)) of Wolfram's New Kind of Science.
    # See: https://www.wolframscience.com/nks/p79--turing-machines/

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

    tm = TapeCentricTuringMachine(n=21, rule_table=rule_table,
                                  initial_head_state=HEAD['up'], initial_head_position=3)

    initial_conditions = [0] * 21

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=tm.network,
                            activity_rule=tm.activity_rule, timesteps=61)

    activities = ntm.get_activities_over_time_as_list(trajectory)
    ntm.plot_grid(activities, node_annotations=tm.head_activities(trajectory), show_grid=True)
