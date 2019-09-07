import netomaton as ntm


if __name__ == "__main__":

    states = {
        'q0': 0,  # initial state
        'q1': 1,
        'q2': 2,
        'q3': 3   # final/accepting state
    }

    # a Pushdown Automata can be thought of as a Network Automaton with a single cell
    adjacencies = [[1]]

    # the Pushdown Automaton starts off in the q0 state
    initial_conditions = [states['q0']]

    # 'Z' is the symbol representing the bottom of the stack
    stack = ['Z']

    # '\n' is the symbol representing the end of the input
    events = "aaabbb\n"

    def pda_rule(n, c, event):
        current_state = n.current_activity
        if current_state == states['q0'] and event == 'a' and stack[-1] == 'Z':
            stack.append('a')
            return states['q1']
        elif current_state == states['q1'] and event == 'a' and stack[-1] == 'a':
            stack.append('a')
            return states['q1']
        elif current_state == states['q1'] and event == 'b' and stack[-1] == 'a':
            stack.pop()
            return states['q2']
        elif current_state == states['q2'] and event == 'b' and stack[-1] == 'a':
            stack.pop()
            return states['q2']
        elif current_state == states['q2'] and event == '\n' and stack[-1] == 'Z':
            return states['q3']
        else:
            raise Exception("input rejected")

    try:
        activities, _ = ntm.evolve(initial_conditions, adjacencies, input=events, activity_rule=pda_rule)
        print("'%s' accepted (final state: %s)" % (events.strip(), activities[-1][0]))
    except Exception:
        print("'%s' rejected!" % events.strip())
