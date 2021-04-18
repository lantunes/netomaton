import math
from .utils import get_activities_over_time_as_list
from .state import State
import numpy as np


def shannon_entropy(string):
    """
    Calculates the Shannon entropy for the given string.

    :param string: any string, such as '000101001', '12402', or 'aBcd1234ef5g'

    :return: a real number representing the Shannon entropy
    """
    symbols = dict.fromkeys(list(string))
    symbol_probabilities = [float(string.count(symbol)) / len(string) for symbol in symbols]
    H = -sum([p_symbol * math.log(p_symbol, 2.0) for p_symbol in symbol_probabilities])
    return H + 0  # add 0 as a workaround so we don't end up with -0.0


def average_node_entropy(trajectory_or_activities):
    """
    Calculates the average node entropy in the given automaton evolution, where entropy is the Shannon entropy.
    The state of a node over time is represented as a string, and its entropy is calculated. The same is done for all
    nodes in this Network Automaton, and the average entropy is returned.

    :param trajectory_or_activities: a list of States that represents the evolution of the automaton, or a list of
                                     lists that represents the evolution of the automaton, where an inner list
                                     represents the activities of the nodes at a given timestep

    :return: a real number representing the average node Shannon entropy
    """
    if len(trajectory_or_activities) is 0:
        raise Exception("there are no activities")
    if isinstance(trajectory_or_activities[0], State):
        # trajectory_or_activities is a trajectory, convert it to an activities list
        activities = get_activities_over_time_as_list(trajectory_or_activities)
    else:
        activities = trajectory_or_activities
    num_cols = len(activities[0])
    entropies = []
    for i in range(0, num_cols):
        node_states_over_time = ''.join([str(x) for x in [y[i] for y in activities]])
        entropy = shannon_entropy(node_states_over_time)
        entropies.append(entropy)
    return np.mean(entropies)


def joint_shannon_entropy(stringX, stringY):
    """
    Calculates the joint Shannon entropy between the given strings, which must be of the same length.

    :param stringX: any string, such as '000101001', '12402', or 'aBcd1234ef5g'

    :param stringY: any string, such as '000101001', '12402', or 'aBcd1234ef5g'

    :return: a real number representing the joint Shannon entropy between the given strings
    """
    X = np.array(list(stringX))
    Y = np.array(list(stringY))
    joint_symbol_probabilities = []
    for x in set(X):
        for y in set(Y):
            joint_symbol_probabilities.append(np.mean(np.logical_and(X == x, Y == y)))
    return sum(-p * np.log2(p) for p in joint_symbol_probabilities if p != 0)


def mutual_information(stringX, stringY):
    """
    Calculates the mutual information between the given strings, which must be of the same length.

    :param stringX: any string, such as '000101001', '12402', or 'aBcd1234ef5g'

    :param stringY: any string, such as '000101001', '12402', or 'aBcd1234ef5g'

    :return: a real number representing the mutual information between the given strings
    """
    return shannon_entropy(stringX) + shannon_entropy(stringY) - joint_shannon_entropy(stringX, stringY)


def average_mutual_information(trajectory_or_activities, temporal_distance=1):
    """
    Calculates the average mutual information between a node and itself at the next n time steps, given by the
    specified temporal distance. A temporal distance of 1 means the next time step.
    For example, consider the following string, '00101010110', which represents the state of a node over 11 time steps.
    The strings which will be used for the computation of the mutual information between a node and itself at the
    next time step are: '0010101011' and '0101010110', since we pair each time-step value with its next value:
    " 00101010110"
    "00101010110 "

    :param trajectory_or_activities: a list of States that represents the evolution of the automaton, or a list of
                                     lists that represents the evolution of the automaton, where an inner list
                                     represents the activities of the nodes at a given timestep

    :param temporal_distance: the size of temporal separation, where the value must be greater than 0 and
                              less than the number of time steps.

    :return: a real number representing the average mutual information between a node and itself at the next time step
    """
    if len(trajectory_or_activities) is 0:
        raise Exception("there are no activities")
    if isinstance(trajectory_or_activities[0], State):
        # trajectory_or_activities is a trajectory, convert it to an activities list
        activities = get_activities_over_time_as_list(trajectory_or_activities)
    else:
        activities = trajectory_or_activities
    num_cols = len(activities[0])
    if not (0 < temporal_distance < num_cols):
        raise Exception("the temporal distance must be greater than 0 and less than the number of time steps")
    mutual_informations = []
    for i in range(0, num_cols):
        node_states_over_time = ''.join([str(x) for x in [y[i] for y in activities]])
        mi = mutual_information(node_states_over_time[:-temporal_distance], node_states_over_time[temporal_distance:])
        mutual_informations.append(mi)
    return np.mean(mutual_informations)
