from abc import abstractmethod

from .topology import cellular_automaton, from_adjacency_matrix
from .utils import get_activities_over_time_as_list


class TuringMachine:
    LEFT = 0
    STAY = 1
    RIGHT = 2

    @abstractmethod
    def network(self):
        pass

    @abstractmethod
    def activity_rule(self, ctx):
        pass


class TapeCentricTuringMachine(TuringMachine):
    """
    A Turing Machine modelled as a Network Automaton with a number of nodes representing the tape (with the same local
    connectivity as an Elementary Cellular Automaton), whose states are mutated as the tape is written to, and separate
    variables for the state and current location of the head.
    """

    def __init__(self, n, rule_table, initial_head_state, initial_head_position):
        self._n = n
        self._rule_table = rule_table
        self._head_history = [(initial_head_state, initial_head_position)]
        self._current_timestep = 1

    @property
    def network(self):
        return cellular_automaton(self._n)

    def activity_rule(self, ctx):
        if ctx.timestep != self._current_timestep:
            self._current_timestep = ctx.timestep
        head_state, head_pos = self._head_history[self._current_timestep - 1]
        node_state = ctx.current_activity
        if ctx.node_label == head_pos:
            try:
                next_head_state, new_node_state, direction = self._rule_table[head_state][node_state]
            except KeyError as err:
                raise Exception("no rule defined for head state %s, input %s" % (head_state, node_state)) from err
            self._head_history.append((next_head_state, ctx.neighbour_labels[direction]))
            return new_node_state
        return node_state

    def head_activities(self, trajectory):
        activities = get_activities_over_time_as_list(trajectory)
        annotations = [[None for _ in range(self._n)] for _ in range(len(activities))]
        for i, h in enumerate(self._head_history):
            annotations[i][h[1]] = str(h[0])
        return annotations


class HeadCentricTuringMachine(TuringMachine):
    """
    A Turing Machine modelled as a Network Automaton with a single node that carries the state of the head, and a
    separate tape that is read from and written to during processing.
    """

    def __init__(self, tape, rule_table, initial_head_state, initial_head_position,
                 terminating_state=None, max_timesteps=None):
        if terminating_state is None and max_timesteps is None:
            raise Exception("a terminating state or the max number of timesteps must be specified")
        self._tape_history = [tape]
        self._rule_table = rule_table
        # the state of the single node in the Network Automaton is a tuple: (head_state, head_position)
        self._initial_conditions = [(initial_head_state, initial_head_position)]
        self._head_pos = initial_head_position
        self._terminating_state = terminating_state
        self._max_timesteps = max_timesteps
        self._halt = False

    @property
    def network(self):
        # a Turing Machine can be thought of as a Network Automaton with a single node
        return from_adjacency_matrix([[1]])

    @property
    def initial_conditions(self):
        return self._initial_conditions

    def activity_rule(self, ctx):
        input_from_tape = ctx.input
        head_state, head_pos = ctx.current_activity
        try:
            next_head_state, val_to_write, direction = self._rule_table[head_state][input_from_tape]
        except KeyError as err:
            raise Exception("no rule defined for head state %s, input %s" % (head_state, input_from_tape)) from err
        new_tape = [i for i in self._tape_history[-1]]
        new_tape[head_pos] = val_to_write
        self._tape_history.append(new_tape)

        if self._terminating_state is not None and next_head_state == self._terminating_state:
            self._halt = True

        self._head_pos = self._next_pos(direction, head_pos)
        return next_head_state, self._head_pos

    def _next_pos(self, direction, head_pos):
        if direction == TuringMachine.LEFT:
            return (head_pos - 1) % len(self._tape_history[-1])
        elif direction == TuringMachine.RIGHT:
            return (head_pos + 1) % len(self._tape_history[-1])
        elif direction == TuringMachine.STAY:
            return head_pos
        else:
            raise Exception("unsupported direction: %s" % direction)

    def input_function(self, t, a, n):
        if self._max_timesteps is not None and len(self._tape_history) == self._max_timesteps:
            return None

        if self._halt:
            return None

        return self._tape_history[-1][self._head_pos]

    def activities_for_plotting(self, trajectory):
        activities = get_activities_over_time_as_list(trajectory)
        head_activities = [[None for _ in range(len(self._tape_history[-1]))] for _ in range(len(self._tape_history))]
        for i, h in enumerate(activities):
            head_activities[i][h[0][1]] = str(h[0][0])

        return self._tape_history, head_activities
