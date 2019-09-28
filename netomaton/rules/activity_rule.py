import numpy as np
from statistics import mode, StatisticsError
from collections import deque


def totalistic_ca(ctx, k, rule):
    """
    The totalistic rule as described in NKS. The average color is mapped to a whole number in [0, k - 1].
    The rule number is in base 10, but interpreted in base k. For a 1-dimensional cellular automaton, there are
    3k - 2 possible average colors in the 3-cell neighbourhood. There are n(k - 1) + 1 possible average colors for a
    k-color cellular automaton with an n-cell neighbourhood.
    :param ctx: the NodeContext for a cell (i.e. node)
    :param k: the number of colors in this cellular automaton, where only 2 <= k <= 36 is supported
    :param rule: the k-color cellular automaton rule number in base 10, interpreted in base k
    :return: the result, a number from 0 to k - 1, of applying the given rule on the given state
    """
    # e.g. np.base_repr(777, base=3) -> '1001210'; the zfill pads the string with zeroes: '1'.zfill(3) -> '001'
    #   Bases greater than 36 not handled in base_repr.
    neighbourhood = np.array(ctx.activities)
    n = neighbourhood.size
    rule_string = np.base_repr(rule, base=k).zfill(n*(k - 1) + 1)
    if len(rule_string) > n*(k - 1) + 1:
        raise Exception("rule number out of range")
    neighbourhood_sum = np.sum(neighbourhood)
    # the rightmost element of the rule is for the average color 0, in NKS convention
    return int(rule_string[n*(k - 1) - neighbourhood_sum], k)


def majority_rule(ctx):
    """
    Returns the value of the most frequent state in the neighbourhood. If all states are equally frequent, then a
    random state is chosen from the neighbourhood.
    :param ctx: the NodeContext for a node
    :return: the new activity for the node with the given neighbourhood
    """
    try:
        return mode(ctx.activities)
    except StatisticsError:
        # a StatisticsError is raised if there is a tie, and there is no single most common element
        return np.random.choice(ctx.activities)


def _bits_to_int(bits):
    total = 0
    for shift, j in enumerate(bits[::-1]):
        if j:
            total += 1 << shift
    return total


def _int_to_bits(num, num_digits):
    converted = list(map(int, bin(num)[2:]))
    return np.pad(converted, (num_digits - len(converted), 0), 'constant')


def shift_to_center(activities, node_indices, node_index):
    center = len(activities) // 2
    shifted = deque(activities)

    def index_of(arr, val):
        return np.where(arr == val)[0][0] if type(arr) == np.ndarray else arr.index(val)
    shifted.rotate(center - index_of(node_indices, node_index))
    return list(shifted)


def binary_ca_rule(ctx, rule, scheme=None):
    """
    Converts the given rule number to a binary representation, and uses this to determine the value to return.
    The process is approximately described as:
    1. convert state to int, so [1,0,1] -> 5, call this state_int
    2. convert rule to binary, so 254 -> [1,1,1,1,1,1,1,0], call this rule_bin_array
    3. new value is rule_bin_array[7 - state_int]
         we subtract 7 from state_int to be consistent with the numbering scheme used in NKS
         in NKS, rule 254 for a 1D binary cellular automaton is described as:
        [1,1,1]  [1,1,0]  [1,0,1]  [1,0,0]  [0,1,1]  [0,1,0]  [0,0,1]  [0,0,0]
           1        1        1        1        1        1        1        0
    If None is provided for the scheme parameter, the neighbourhoods are listed in lexicographic order (the reverse of
    the NKS convention). If 'nks' is provided for the scheme parameter, the NKS convention is used for listing the
    neighbourhoods.
    :param ctx: the NodeContext for a cell (i.e. node); the activities are a binary array of length 2r + 1
    :param rule: an int indicating the cellular automaton rule number
    :param scheme: can be None (default) or 'nks'; if 'nks' is given, the rule numbering scheme used in NKS is used
    :return: the result, 0 or 1, of applying the given rule on the given state
    """
    # shift the activities so that the current cell's activity is in the center
    activities = shift_to_center(ctx.activities, ctx.neighbour_indices, ctx.node_index)
    state_int = _bits_to_int(activities)
    n = 2**len(activities)
    rule_bin_array = _int_to_bits(rule, n)
    if scheme == 'nks':
        return rule_bin_array[(n-1) - state_int]
    return rule_bin_array[state_int]


def nks_ca_rule(ctx, rule):
    """
    A convenience function, that calls binary_rule with scheme = 'nks'.
    :param ctx: the NodeContext for a cell (i.e. node); the activities are a binary array of length 2r + 1
    :param rule: an int indicating the cellular automaton rule number
    :return:
    """
    return binary_ca_rule(ctx, rule, scheme='nks')


def game_of_life_rule(ctx):
    activities = ctx.activities
    center_cell = activities[len(activities) // 2]
    total = np.sum(activities)
    if center_cell == 1:
        if total - 1 < 2:
            return 0  # Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
        if total - 1 == 2 or total - 1 == 3:
            return 1  # Any live cell with two or three live neighbours lives on to the next generation.
        if total - 1 > 3:
            return 0  # Any live cell with more than three live neighbours dies, as if by overpopulation.
    else:
        if total == 3:
            return 1  # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        else:
            return 0
