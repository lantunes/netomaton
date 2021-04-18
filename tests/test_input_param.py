import numpy as np

import netomaton as ntm


class TestInputParam:

    # test the input parameter using a Finite State Machine
    def test_fsm(self):

        states = {'locked': 0, 'unlocked': 1}
        transitions = {'PUSH': 'p', 'COIN': 'c'}

        network = ntm.topology.from_adjacency_matrix([[1]])

        initial_conditions = [states['locked']]

        events = "cpcpp"

        def fsm_rule(ctx):
            if ctx.input == transitions['PUSH']:
                return states['locked']
            else:
                # COIN event
                return states['unlocked']

        trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                                input=events, activity_rule=fsm_rule)

        activities = ntm.get_activities_over_time_as_list(trajectory)
        np.testing.assert_equal([[0], [1], [0], [1], [0], [0]], activities)
