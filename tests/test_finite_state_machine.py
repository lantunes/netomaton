import netomaton as ntm
from .rule_test import *


class TestFiniteStateMachine(RuleTest):

    def test_fsm(self):
        states = {'locked': 0, 'unlocked': 1}
        transitions = {'PUSH': 'p', 'COIN': 'c'}

        # a FSM can be thought of as a Network Automaton with a single node
        adjacency_matrix = [[1]]

        # the FSM starts off in the Locked state
        initial_conditions = [states['locked']]

        events = "cpcpp"

        def fsm_rule(ctx):
            if ctx.input == transitions['PUSH']:
                return states['locked']
            else:
                # COIN event
                return states['unlocked']

        activities, _ = ntm.evolve_2(initial_conditions=initial_conditions, topology=adjacency_matrix,
                                     input=events, activity_rule=fsm_rule)

        expected = [[0], [1], [0], [1], [0], [0]]
        np.testing.assert_equal(expected, activities)
