from .asynchronous_rule import *
from .topology import from_adjacency_matrix
import numpy as np


class HopfieldNet:
    """
    The Hopfield net implemented here expects bipolar ({-1,1}), and not binary ({0,1}), values. It consists of a
    training step, where the weights of the adjacency matrix are established, using a simple Hebbian learning rule,
    and an evaluation step, in which a starting pattern is evolved for a specified number of timesteps. The final state
    of the network should settle into one of the training patterns.
    """
    def __init__(self, n):
        self._activity_rule = AsynchronousRule(activity_rule=self._rule, n=n, randomize_each_cycle=True)
        self._num_nodes = n

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
        self._network = from_adjacency_matrix(self._adjacency_matrix)

    def _rule(self, ctx):
        """
        Peforms a linear combination of the neighbourhood activities and the corresponding weights. If the combined
        value is greater than or equal to 0, then 1 is returned, otherwise -1 is returned.
        :param ctx: the NodeContext; note that the neighbourhood of the node, in this case, does not include the
                    node itself
        :return: the new value of the node
        """
        V = 0
        for neighbour_label in ctx.neighbour_labels:
            V += ctx.connection_states[neighbour_label][0]["weight"] * ctx.activities[neighbour_label]
        return 1 if V >= 0 else -1

    @property
    def activity_rule(self):
        return self._activity_rule

    @property
    def network(self):
        return self._network

    @property
    def adjacency_matrix(self):
        return self._adjacency_matrix

    @property
    def num_nodes(self):
        return self._num_nodes
