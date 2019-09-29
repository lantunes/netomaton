import netomaton as ntm
import numpy as np


if __name__ == "__main__":

    adjacency_matrix = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1]
    ]

    initial_conditions = [1, 2, 2, 1]

    def connectivity_rule(ctx):
        connectivity_map = {}
        new_idx = 0
        for idx, activity in enumerate(ctx.last_activities):
            right_idx = idx + 1
            if right_idx == len(ctx.last_activities):
                continue
            right_activity = ctx.last_activities[right_idx]

            if activity == 2 and right_activity == 2:
                connectivity_map[new_idx] = {new_idx: 1}
                if new_idx > 0:
                    connectivity_map[new_idx][new_idx-1] = 1
                new_idx += 1
                connectivity_map[new_idx] = {(new_idx-1): 1, new_idx: 1}
                new_idx += 1

            if activity == 2 and right_activity == 1:
                connectivity_map[new_idx] = {new_idx: 1}
                if new_idx > 0:
                    connectivity_map[new_idx][new_idx - 1] = 1
                new_idx += 1

            if activity == 1 and right_activity == 2:
                connectivity_map[new_idx] = {new_idx: 1}
                if new_idx > 0:
                    connectivity_map[new_idx][new_idx - 1] = 1
                new_idx += 1
                connectivity_map[new_idx] = {(new_idx - 1): 1, new_idx: 1}
                new_idx += 1

            if activity == 1 and right_activity == 1:
                continue

        adjacency = np.zeros((len(connectivity_map), len(connectivity_map)))
        for row, vals in connectivity_map.items():
            for col, val in vals.items():
                adjacency[row][col] = val

        return adjacency


    def activity_rule(ctx):
        right_index = ctx.node_index + 1

        if not ctx.has_node(right_index):
            ctx.remove(ctx.node_index)
            return 0

        current = ctx.current_activity
        right = ctx.activity_of(right_index)

        if current == 2 and right == 2:
            ctx.insert(right_index, 2)
            return 2

        if current == 2 and right == 1:
            return 1

        if current == 1 and right == 2:
            ctx.insert(right_index, 1)
            return 2

        if current == 1 and right == 1:
            ctx.remove(ctx.node_index)
            return 0


    activities, connectivities = ntm.evolve(initial_conditions, adjacency_matrix, connectivity_rule=connectivity_rule,
                                            activity_rule=activity_rule, timesteps=13)

    max_len = np.max([len(a) for a in activities])
    padded = np.asarray([np.pad(a, (0, max_len - len(a)), 'constant', constant_values=0) for a in activities])

    ntm.plot_grid(padded, show_grid=True)
