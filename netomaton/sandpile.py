import numpy as np

from .topology import cellular_automaton2d


class Sandpile:
    def __init__(self, rows, cols, is_closed_boundary=True):
        self._K = 4  # this value is hard-coded because the neighbourhood type, "von Neumann", is fixed
        self._network = cellular_automaton2d(rows=rows, cols=cols, neighbourhood="von Neumann")
        self._boundary_indices = self._get_boundary_indices((rows, cols))
        self._is_closed_boundary = is_closed_boundary

    def _get_boundary_indices(self, shape):
        m = np.arange(shape[0]*shape[1]).reshape(shape)
        return np.concatenate((m[0], m[-1], m[:, 0], m[:, -1]), axis=None)

    def activity_rule(self, ctx):
        if self._is_closed_boundary and ctx.node_label in self._boundary_indices:
            return 0  # closed boundary conditions

        new_activity = ctx.current_activity

        neighbour_activities = list(ctx.neighbourhood_activities)
        neighbour_activities.pop(ctx.neighbour_labels.index(ctx.node_label))

        for neighbour_activity in neighbour_activities:
            if neighbour_activity >= self._K:
                new_activity += 1

        if ctx.current_activity >= self._K:
            new_activity -= self._K

        return new_activity

    @property
    def network(self):
        return self._network
