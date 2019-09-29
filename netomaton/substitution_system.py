import numpy as np


class SubstitutionSystem:
    def __init__(self, rules, n):
        self._rules = rules
        self._adjacency_matrix = self._init_adjacency_matrix(n)

    def _init_adjacency_matrix(self, n):
        neighbourhood_size = len(next(iter(self._rules)))
        adjacency_matrix = [[1] + [0]*(n-1)]
        idx = 1
        for i in range(1, n):
            row = [0 for _ in range(n)]
            row[idx] = 1
            for j in range(1, neighbourhood_size):
                next_idx = idx - j
                if next_idx >= 0:
                    row[next_idx] = 1
            idx += 1
            adjacency_matrix.append(row)
        return adjacency_matrix

    def _get_state(self, ctx):
        state = ""
        for idx in ctx.neighbour_indices:
            state += str(ctx.activity_of(idx))
        return state

    def activity_rule(self, ctx):
        current_state = self._get_state(ctx)
        if not current_state in self._rules:
            ctx.remove(ctx.node_index)
            return 0

        new_state = self._rules[current_state]
        if len(new_state) == 0:
            ctx.remove(ctx.node_index)
            return 0

        for i in range(1, len(new_state)):
            ctx.insert(ctx.node_index+i, int(new_state[i]))
        return int(new_state[0])

    def connectivity_rule(self, ctx):
        neighbourhood_size = len(next(iter(self._rules)))
        activities = ''.join([str(a) for a in ctx.last_activities])

        connectivity_map = {}
        new_idx = 0
        for idx, activity in enumerate(activities):
            state = activities[idx:(idx+neighbourhood_size)]
            if not state in self._rules:
                continue

            new_state = self._rules[state]
            if len(new_state) == 0:
                continue

            for i in range(len(new_state)):
                connectivity_map[new_idx] = {new_idx: 1}
                for j in range(1, neighbourhood_size):
                    next_idx = new_idx - j
                    if next_idx >= 0:
                        connectivity_map[new_idx][next_idx] = 1
                new_idx += 1

        adjacency = np.zeros((len(connectivity_map), len(connectivity_map)))
        for row, vals in connectivity_map.items():
            for col, val in vals.items():
                adjacency[row][col] = val

        return adjacency

    @property
    def adjacency_matrix(self):
        return self._adjacency_matrix

    def pad(self, activities):
        max_len = np.max([len(a) for a in activities])
        return np.asarray([np.pad(a, (0, max_len - len(a)), 'constant', constant_values=0) for a in activities])
