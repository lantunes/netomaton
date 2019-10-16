import netomaton as ntm
from netomaton import TuringMachine, HeadCentricTuringMachine, TapeCentricTuringMachine
from .rule_test import *


class TestTuringMachine(RuleTest):

    def test_turing_machine1(self):
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
        tm = HeadCentricTuringMachine(tape=[0] * 21, rule_table=rule_table,
                                      initial_head_state=HEAD['up'], initial_head_position=3, max_timesteps=61)
        activities, _ = ntm.evolve(tm.initial_conditions, tm.adjacency_matrix,
                                   activity_rule=tm.activity_rule, input=tm.input_function)
        tape_history, head_activities = tm.activities_for_plotting(activities)

        expected_activities = [[(1, 3)], [(2, 4)], [(2, 3)], [(1, 2)], [(2, 3)], [(1, 2)], [(1, 3)], [(1, 4)],
                               [(1, 5)], [(2, 6)], [(2, 5)], [(1, 4)], [(2, 5)], [(1, 4)], [(1, 5)], [(1, 6)],
                               [(1, 7)], [(2, 8)], [(2, 7)], [(1, 6)], [(2, 7)], [(1, 6)], [(1, 7)], [(1, 8)],
                               [(1, 9)], [(2, 10)], [(2, 9)], [(1, 8)], [(2, 9)], [(1, 8)], [(1, 9)], [(1, 10)],
                               [(1, 11)], [(2, 12)], [(2, 11)], [(1, 10)], [(2, 11)], [(1, 10)], [(1, 11)], [(1, 12)],
                               [(1, 13)], [(2, 14)], [(2, 13)], [(1, 12)], [(2, 13)], [(1, 12)], [(1, 13)], [(1, 14)],
                               [(1, 15)], [(2, 16)], [(2, 15)], [(1, 14)], [(2, 15)], [(1, 14)], [(1, 15)], [(1, 16)],
                               [(1, 17)], [(2, 18)], [(2, 17)], [(1, 16)], [(2, 17)]]
        np.testing.assert_equal(expected_activities, activities.tolist())
        expected_tape_history = self._convert_to_list_of_lists("turing_machine1-tape.ca")
        np.testing.assert_equal(expected_tape_history, tape_history)
        expected_head_activities = self._convert_to_list_of_lists("turing_machine1-head.ca", strings=True)
        np.testing.assert_equal(expected_head_activities, head_activities)

    def test_turing_machine1b(self):
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
        tm = HeadCentricTuringMachine(tape=[CELL[t] for t in tape], rule_table=rule_table,
                                      initial_head_state=HEAD['q0'], initial_head_position=2,
                                      terminating_state=HEAD['q6'], max_timesteps=50)
        activities, _ = ntm.evolve(tm.initial_conditions, tm.adjacency_matrix, activity_rule=tm.activity_rule,
                                   input=tm.input_function)
        tape_history, head_activities = tm.activities_for_plotting(activities)

        expected_activities = [[(0, 2)], [(1, 3)], [(1, 4)], [(2, 5)], [(2, 6)], [(3, 5)], [(3, 4)], [(3, 3)], [(3, 2)],
                               [(0, 3)], [(1, 4)], [(1, 5)], [(2, 6)], [(2, 7)], [(3, 6)], [(3, 5)], [(3, 4)], [(3, 3)],
                               [(0, 4)], [(4, 3)], [(4, 2)], [(4, 1)], [(5, 2)], [(5, 3)], [(5, 4)], [(5, 5)], [(5, 6)],
                               [(5, 7)], [(5, 8)], [(6, 8)]]
        np.testing.assert_equal(expected_activities, activities.tolist())
        expected_tape_history = self._convert_to_list_of_lists("turing_machine1b-tape.ca")
        np.testing.assert_equal(expected_tape_history, tape_history)
        expected_head_activities = self._convert_to_list_of_lists("turing_machine1b-head.ca", strings=True)
        np.testing.assert_equal(expected_head_activities, head_activities)

    def test_turing_machine1c(self):
        HEAD = {"up": 1, "down": 2}
        CELL = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
        rule_table = {
            HEAD['up']: {
                CELL['a']: [HEAD['up'], CELL['b'], TuringMachine.LEFT],
                CELL['b']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
                CELL['c']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
                CELL['d']: [HEAD['down'], CELL['e'], TuringMachine.RIGHT],
                CELL['e']: [HEAD['down'], CELL['d'], TuringMachine.LEFT]
            },
            HEAD['down']: {
                CELL['a']: [HEAD['up'], CELL['d'], TuringMachine.LEFT],
                CELL['b']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
                CELL['c']: [HEAD['up'], CELL['e'], TuringMachine.RIGHT],
                CELL['d']: [HEAD['down'], CELL['e'], TuringMachine.RIGHT],
                CELL['e']: [HEAD['down'], CELL['c'], TuringMachine.LEFT]
            }
        }
        tape = "bbbbbbaeaaaaaaa"
        tm = HeadCentricTuringMachine(tape=[CELL[t] for t in tape], rule_table=rule_table,
                                      initial_head_state=HEAD['up'], initial_head_position=8, max_timesteps=58)
        activities, _ = ntm.evolve(tm.initial_conditions, tm.adjacency_matrix, activity_rule=tm.activity_rule,
                                   input=tm.input_function)
        tape_history, head_activities = tm.activities_for_plotting(activities)

        expected_activities = [[(1, 8)], [(1, 7)], [(2, 6)], [(1, 5)], [(1, 6)], [(2, 7)], [(2, 8)], [(1, 9)], [(1, 8)],
                               [(1, 7)], [(2, 6)], [(2, 5)], [(1, 4)], [(1, 5)], [(2, 6)], [(1, 7)], [(2, 8)], [(1, 9)],
                               [(1, 10)], [(1, 9)], [(1, 8)], [(1, 7)], [(2, 6)], [(2, 5)], [(2, 4)], [(1, 3)], [(1, 4)],
                               [(2, 5)], [(1, 6)], [(1, 7)], [(2, 8)], [(1, 9)], [(1, 10)], [(1, 11)], [(1, 10)], [(1, 9)],
                               [(1, 8)], [(1, 7)], [(2, 6)], [(1, 5)], [(2, 4)], [(2, 3)], [(1, 2)], [(1, 3)], [(2, 4)],
                               [(1, 5)], [(2, 6)], [(2, 7)], [(2, 8)], [(1, 9)], [(1, 10)], [(1, 11)], [(1, 12)],
                               [(1, 11)], [(1, 10)], [(1, 9)], [(1, 8)], [(1, 7)]]
        np.testing.assert_equal(expected_activities, activities.tolist())
        expected_tape_history = self._convert_to_list_of_lists("turing_machine1c-tape.ca")
        np.testing.assert_equal(expected_tape_history, tape_history)
        expected_head_activities = self._convert_to_list_of_lists("turing_machine1c-head.ca", strings=True)
        np.testing.assert_equal(expected_head_activities, head_activities)

    def test_turing_machine2(self):
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
        activities, _ = ntm.evolve(initial_conditions, tm.adjacency_matrix, activity_rule=tm.activity_rule,
                                   timesteps=61)
        head_activities = tm.head_activities(activities)

        expected_activities = self._convert_to_list_of_lists("turing_machine2.ca")
        np.testing.assert_equal(expected_activities, activities.tolist())
        expected_head_activities = self._convert_to_list_of_lists("turing_machine2-head.ca", strings=True)
        np.testing.assert_equal(expected_head_activities, head_activities)

    def test_turing_machine2b(self):
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
        tm = TapeCentricTuringMachine(n=len(tape), rule_table=rule_table,
                                      initial_head_state=HEAD['q0'], initial_head_position=2)
        initial_conditions = [CELL[t] for t in tape]
        activities, _ = ntm.evolve(initial_conditions, tm.adjacency_matrix, activity_rule=tm.activity_rule,
                                   timesteps=61)
        head_activities = tm.head_activities(activities)

        expected_activities = self._convert_to_list_of_lists("turing_machine2b.ca")
        np.testing.assert_equal(expected_activities, activities.tolist())
        expected_head_activities = self._convert_to_list_of_lists("turing_machine2b-head.ca", strings=True)
        np.testing.assert_equal(expected_head_activities, head_activities)

    def test_turing_machine2c(self):
        HEAD = {"up": 1, "down": 2}
        CELL = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
        rule_table = {
            HEAD['up']: {
                CELL['a']: [HEAD['up'], CELL['b'], TuringMachine.LEFT],
                CELL['b']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
                CELL['c']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
                CELL['d']: [HEAD['down'], CELL['e'], TuringMachine.RIGHT],
                CELL['e']: [HEAD['down'], CELL['d'], TuringMachine.LEFT]
            },
            HEAD['down']: {
                CELL['a']: [HEAD['up'], CELL['d'], TuringMachine.LEFT],
                CELL['b']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
                CELL['c']: [HEAD['up'], CELL['e'], TuringMachine.RIGHT],
                CELL['d']: [HEAD['down'], CELL['e'], TuringMachine.RIGHT],
                CELL['e']: [HEAD['down'], CELL['c'], TuringMachine.LEFT]
            }
        }
        tape = "bbbbbbaeaaaaaaa"
        tm = TapeCentricTuringMachine(n=len(tape), rule_table=rule_table,
                                      initial_head_state=HEAD['up'], initial_head_position=8)
        initial_conditions = [CELL[t] for t in tape]
        activities, _ = ntm.evolve(initial_conditions, tm.adjacency_matrix, activity_rule=tm.activity_rule,
                                   timesteps=58)
        head_activities = tm.head_activities(activities)

        expected_activities = self._convert_to_list_of_lists("turing_machine2c.ca")
        np.testing.assert_equal(expected_activities, activities.tolist())
        expected_head_activities = self._convert_to_list_of_lists("turing_machine2c-head.ca", strings=True)
        np.testing.assert_equal(expected_head_activities, head_activities)
