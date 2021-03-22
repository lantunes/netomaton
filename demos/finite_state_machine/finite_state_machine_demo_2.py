import netomaton as ntm


if __name__ == "__main__":

    # The "Turnstile" FSM in this case contains two states: Locked (0) and Unlocked (1).
    # It can undergo two kinds of transitions: Push ("p") and Coin ("c").
    # The machine starts off in the Locked state.
    # If a push is given in the Locked state, it remains Locked.
    # If a coin is given in the Locked state, it transitions to Unlocked.
    # If a push is given in the Unlocked state, it transitions to Locked.
    # If a coin is given in the Unlocked state, it remains Unlocked.

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

    activities, _ = ntm.evolve_2(initial_conditions, adjacency_matrix, input=events, activity_rule=fsm_rule)

    print("final state: %s" % activities[-1][0])

    ntm.plot_grid(activities)
