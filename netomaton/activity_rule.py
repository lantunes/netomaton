import numpy as np
from statistics import mode, StatisticsError


class ActivityRule:
    @staticmethod
    def totalistic_ca(neighbourhood, k, rule):
        """
        The totalistic rule as described in NKS. The average color is mapped to a whole number in [0, k - 1].
        The rule number is in base 10, but interpreted in base k. For a 1-dimensional cellular automaton, there are
        3k - 2 possible average colors in the 3-cell neighbourhood. There are n(k - 1) + 1 possible average colors for a
        k-color cellular automaton with an n-cell neighbourhood.
        :param neighbourhood: the automaton neighbourhood for a cell
        :param k: the number of colors in this cellular automaton, where only 2 <= k <= 36 is supported
        :param rule: the k-color cellular automaton rule number in base 10, interpreted in base k
        :return: the result, a number from 0 to k - 1, of applying the given rule on the given state
        """
        # e.g. np.base_repr(777, base=3) -> '1001210'; the zfill pads the string with zeroes: '1'.zfill(3) -> '001'
        #   Bases greater than 36 not handled in base_repr.
        neighbourhood = np.array(neighbourhood.activities)
        n = neighbourhood.size
        rule_string = np.base_repr(rule, base=k).zfill(n*(k - 1) + 1)
        if len(rule_string) > n*(k - 1) + 1:
            raise Exception("rule number out of range")
        neighbourhood_sum = np.sum(neighbourhood)
        # the rightmost element of the rule is for the average color 0, in NKS convention
        return int(rule_string[n*(k - 1) - neighbourhood_sum], k)

    @staticmethod
    def majority_rule(neighbourhood):
        """
        Returns the value of the most frequent state in the neighbourhood. If all states are equally frequent, then a
        random state is chosen from the neighbourhood.
        :param neighbourhood: the automaton neighbourhood for a cell
        :return: the new activity for the cell with the given neighbourhood
        """
        try:
            return mode(neighbourhood.activities)
        except StatisticsError:
            # a StatisticsError is raised if there is a tie, and there is no single most common element
            return np.random.choice(neighbourhood.activities)