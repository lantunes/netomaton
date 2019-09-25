
class ReversibleRule:
    """
    An automaton rule explicitly set up to be reversible.
    """
    def __init__(self, activity_rule):
        """
        Creates a reversible automata rule by taking into consideration the previous state of a
        cell, by taking the XOR of the rule's normal output with the previous state to get the new state.
        Note that this class works only for automata where the state of a cell is binary.
        :param activity_rule: the automata rule to be used
        """
        self._activity_rule = activity_rule

    def activity_rule(self, n, c, t):
        regular_result = self._activity_rule(n, c, t)
        new_result = regular_result ^ n.past_activity_of(c)
        return new_result
