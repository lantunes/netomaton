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

    # a FSM can be thought of as a Network Automaton with a single cell
    adjacencies = [[1]]

    # the FSM starts off in the Locked state
    initial_conditions = [0]

    events = " cpcpp"

    def fsm_rule(n, c, t):
        event = events[t]
        if event == transitions['PUSH']:
            return states['locked']
        else:
            # COIN event
            if c == states['locked']:
                return states['unlocked']
            return states['unlocked']

    activities, _ = ntm.evolve(initial_conditions, adjacencies,
                               timesteps=len(events), activity_rule=fsm_rule)

    ntm.plot_grid(activities)
