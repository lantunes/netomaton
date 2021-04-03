import numpy as np


class SubstitutionSystem:
    def __init__(self, rules, n):
        self._rules = rules
        self._neighbourhood_size = self._get_neighbourhood_size(rules)
        self._connectivity_map = self._init_connectivity_map(n)
        self._last_node_index = n - 1
        self._num_nodes_added = 0
        self._last_timestep = 0

    def _get_neighbourhood_size(self, rules):
        neighbourhood_size = len(next(iter(rules)))
        for key in rules:
            if len(key) != neighbourhood_size:
                raise Exception("all keys in the rule map must be the same length")
        return neighbourhood_size

    def _init_connectivity_map(self, n):
        # since we require Python 3.6, and dicts respect insertion order, we're using a plain dict here
        # (even though the 3.6 language spec doesn't officially support it)
        connectivity_map = {}
        for i in range(n):
            node_map = {i: [{}]}
            for j in range(1, self._neighbourhood_size):
                if (i + j) < n:
                    node_map[i + j] = [{}]
            connectivity_map[i] = node_map
        return connectivity_map

    def activity_rule(self, ctx):
        ctx.remove_node(ctx.node_label)

        self._update_last_timestep(ctx)

        if len(ctx.neighbour_labels) != self._neighbourhood_size:
            return

        current_state = self._get_state(ctx)
        new_state = self._rules[current_state]

        for i, state in enumerate(new_state):
            self._last_node_index += 1
            new_node_label = self._last_node_index
            self._num_nodes_added += 1
            outgoing_links = {}
            for j in range(0, min(self._num_nodes_added, self._neighbourhood_size)):
                outgoing_links[new_node_label - j] = [{}]
            ctx.add_node(int(state), outgoing_links, new_node_label)

        # we return None here, since the graph has been re-written through the context, and the newly added node(s)
        #  carry the state information

    def _update_last_timestep(self, ctx):
        if self._last_timestep != ctx.timestep:
            self._num_nodes_added = 0
        self._last_timestep = ctx.timestep

    def _get_state(self, ctx):
        state = ""
        for neighbour in ctx.neighbour_labels:
            state += str(ctx.activity_of(neighbour))
        return state

    @property
    def connectivity_map(self):
        return self._connectivity_map

    def pad(self, activities):
        activities = [[activities[k][e] for e in sorted(activities[k])] for k in sorted(activities)]
        max_len = np.max([len(a) for a in activities])
        return np.asarray([np.pad(a, (0, max_len - len(a)), 'constant', constant_values=0) for a in activities])
