

class ReversibleRule:
    """
    An automaton rule explicitly set up to be reversible.
    """
    def __init__(self, activity_rule):
        """
        Creates a reversible automata rule by taking into consideration the previous state of a
        node, by taking the XOR of the rule's normal output with the previous state to get the new state.
        Note that this class works only for automata where the state of a node is binary.
        :param activity_rule: the automata rule to be used
        """
        self._activity_rule = activity_rule

    def __call__(self, ctx):
        regular_result = self._activity_rule(ctx)
        new_result = regular_result ^ ctx.past_activity_of(ctx.node_label)
        return new_result
