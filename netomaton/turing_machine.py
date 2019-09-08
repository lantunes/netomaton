from .network import cellular_automaton


class TuringMachine:
    LEFT = 0
    STAY = 1
    RIGHT = 2

    @property
    def adjacencies(self):
        pass

    def activity_rule(self, n, c, t):
        pass


class TapeCentricTuringMachine(TuringMachine):
    """
    A Turing Machine modelled as a Network Automaton with a number of cells representing the tape (with the same local
    connectivity as an Elementary Cellular Automaton), whose states are mutated as the tape is written to, and separate
    variables for the state and current location of the head.
    """

    def __init__(self, num_cells, rule_table, initial_head_state, initial_head_position):
        self._num_cells = num_cells
        self._rule_table = rule_table
        self._head_history = [(initial_head_state, initial_head_position)]
        self._current_timestep = 1

    @property
    def adjacencies(self):
        return cellular_automaton(self._num_cells)

    def activity_rule(self, n, c, t):
        if t != self._current_timestep:
            self._current_timestep = t
        head_state, head_pos = self._head_history[self._current_timestep - 1]
        cell_state = n.current_activity
        if c == head_pos:
            next_head_state, new_cell_state, pos = self._rule_table[head_state][cell_state]
            self._head_history.append((next_head_state, n.neighbour_indices[pos]))
            return new_cell_state
        return cell_state

    def head_activities(self, activities):
        annotations = [[None for _ in range(self._num_cells)] for _ in range(len(activities))]
        for i, h in enumerate(self._head_history):
            annotations[i][h[1]] = str(h[0])
        return annotations


class HeadCentricTuringMachine(TuringMachine):
    """
    A Turing Machine modelled as a Network Automaton with a single cell that carries the state of the head, and a
    separate tape that is read from and written to during processing.
    """
    def __init__(self):
        # TODO
        pass
