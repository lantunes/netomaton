import numpy as np
from .rules import *


class AsynchronousRule:
    """
    Creates an asynchronous automaton rule with a cyclic update scheme. Also known as a sequential cellular
    automaton rule, in NKS. This rule wraps a given rule, making the given rule asynchronous. To learn more about
    the details of sequential cellular automata, see the Chapter 9, Section 10 Notes on Sequential cellular
    automata in NKS.
    """
    def __init__(self, activity_rule, update_order=None, n=None, randomize_each_cycle=False):
        """
        Constructs an asynchronous rule out of a given rule. Either the `update_order` or `n` parameter must be
        specified. If no `update_order` is given, then the `n` parameter must be specified, and an update order
        list will be constructed and shuffled.
        :param activity_rule: the rule that will be made asynchronous
        :param update_order: a list containing the indices of the nodes in the Network Automaton, specifying the update
                             order; only the nodes specified in the list will be updated
        :param n: the total number of nodes in the Network Automaton
        :param randomize_each_cycle: whether to shuffle the update order list after each complete cycle
        """
        if update_order is None and n is None:
            raise Exception("either update_order or n must be specified")
        self._activity_rule = activity_rule
        if update_order is not None:
            self._update_order = update_order
        else:
            self._shuffle_update_order(n)
        self._curr = 0
        self._num_applied = 0
        self._randomize_each_cycle = randomize_each_cycle

    def _shuffle_update_order(self, n):
        self._update_order = np.arange(n)
        np.random.shuffle(self._update_order)
        self._update_order = self._update_order.tolist()

    def __call__(self, ctx):
        if ctx.node_label in self._update_order:
            self._num_applied += 1
        if not self._should_update(ctx.node_label):
            self._check_for_end_of_cycle()
            return ctx.current_activity
        self._check_for_end_of_cycle()
        return self._activity_rule(ctx)

    def _should_update(self, c,):
        return c == self._update_order[self._curr]

    def _check_for_end_of_cycle(self):
        if self._num_applied == len(self._update_order):
            self._curr = (self._curr + 1) % len(self._update_order)
            self._num_applied = 0
            if self._randomize_each_cycle:
                self._shuffle_update_order(len(self._update_order))
