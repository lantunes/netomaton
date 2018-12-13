
class ReversibleRule:
    """
    An automaton rule explicitly set up to be reversible.
    """
    def __init__(self, initial_conditions, activity_rule):
        """
        Creates a reversible automata rule by taking into consideration the previous state of a
        cell, by taking the XOR of the rule's normal output with the previous state to get the new state.
        Note that this class works only for automata where the state of a cell is binary.
        :param initial_conditions: a vector representing the initial previous state of the cells, consisting of binary values
        :param activity_rule: the automata rule to be used
        """
        self._previous_states = list(initial_conditions)
        self._activity_rule = activity_rule

    def activity_rule(self, n, c, t):
        regular_result = self._activity_rule(n, c, t)
        new_result = regular_result ^ self._previous_states[c]
        self._previous_states[c] = n.current_activity
        return new_result
