import netomaton as ntm
from .rule_test import *


class TestPushdownAutomata(RuleTest):

    def test_pushdown(self):
        states = {
            'q0': 0,  # initial state
            'q1': 1,
            'q2': 2,
            'q3': 3  # final/accepting state
        }

        # a Pushdown Automaton can be thought of as a Network Automaton with a single node
        network = ntm.topology.from_adjacency_matrix([[1]])

        # the Pushdown Automaton starts off in the q0 state
        initial_conditions = [states['q0']]

        # 'Z' is the symbol representing the bottom of the stack
        stack = ['Z']

        # '\n' is the symbol representing the end of the input
        events = "aaabbb\n"

        def pda_rule(ctx):
            current_state = ctx.current_activity
            if current_state == states['q0'] and ctx.input == 'a' and stack[-1] == 'Z':
                stack.append('a')
                return states['q1']
            elif current_state == states['q1'] and ctx.input == 'a' and stack[-1] == 'a':
                stack.append('a')
                return states['q1']
            elif current_state == states['q1'] and ctx.input == 'b' and stack[-1] == 'a':
                stack.pop()
                return states['q2']
            elif current_state == states['q2'] and ctx.input == 'b' and stack[-1] == 'a':
                stack.pop()
                return states['q2']
            elif current_state == states['q2'] and ctx.input == '\n' and stack[-1] == 'Z':
                return states['q3']
            else:
                raise Exception("input rejected")

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                                input=events, activity_rule=pda_rule)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        expected = [[0], [1], [1], [1], [2], [2], [2], [3]]
        np.testing.assert_equal(expected, activities)
