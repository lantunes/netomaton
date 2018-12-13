from .asynchronous_rule import *
import numpy as np


class HopfieldNet:
    """
    The Hopfield net implemented here expects bipolar ({-1,1}), and not binary ({0,1}), values. It consists of a
    training step, where the weights of the adjacency matrix are established, using a simple Hebbian learning rule,
    and an evaluation step, in which a starting pattern is evolved for a specified number of timesteps. The final state
    of the network should settle into one of the training patterns.
    """
    def __init__(self, num_cells):
        self._activity_rule = AsynchronousRule(apply_rule=self._rule, num_cells=num_cells).activity_rule
        self._num_cells = num_cells

    def train(self, P):
        """
        The training set consists of patterns to be learned by this net. The patterns should be composed of
        bipolar ({-1,1}), and not binary ({0,1}), values. The learned weights will be stored in, and comprise, the
        adjacency matrix. Therefore, before the network can be used to evaluate a pattern, it must be trained.
        :param P: the set of training patterns, as a list of lists
        """
        self._adjacency_matrix = np.zeros((len(P[0]), len(P[0])), dtype=np.int)
        for p in P:
            for i in range(len(p)):
                for j in range(len(p)):
                    if i ==j:
                        self._adjacency_matrix[i, j] = 0
                    else:
                        self._adjacency_matrix[i, j] += p[i]*p[j]

    def _rule(self, n, c, t):
        """
        Peforms a linear combination of the neighbourhood activities and the corresponding weights. If the combined
        value is greater than or equal to 0, then 1 is returned, otherwise -1 is returned.
        :param n: the neighbourhood of the cell, which, in this case, does not include the cell itself
        :param c: the index of the cell that this function is being evaluated for
        :param t: the timestep of the automaton evolution
        :return: the new value of the cell
        """
        V = 0
        for i, _ in enumerate(n.activities):
            V += n.weights[i] * n.activities[i]
        return 1 if V >= 0 else -1

    @property
    def activity_rule(self):
        return self._activity_rule

    @property
    def adjacency_matrix(self):
        return self._adjacency_matrix