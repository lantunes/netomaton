import netomaton as ntm
import numpy as np
import math
import csv


def read_weights(fname):
    weights = {}
    with open(fname, "rt") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            node2 = "%sh" % i
            for j, weight in enumerate(line):
                node1 = "%sv" % j
                if node1 not in weights:
                    weights[node1] = {}
                weights[node1][node2] = {"weight": float(weight)}
    return weights


def read_biases(fname, suffix):
    biases = {}
    with open(fname, "rt") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            biases[str(i)+suffix] = float(line[0])
    return biases


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def initialize_rbm(v_nodes, h_nodes, v_biases, h_biases):
    initial_conditions = {}
    for node in v_nodes:
        initial_conditions[node] = (np.random.choice([0, 1]), v_biases[node])
    for node in h_nodes:
        initial_conditions[node] = (0, h_biases[node])
    return initial_conditions


def get_visible_activities(trajectory):
    visible_activities = []
    for state in trajectory:
        activities = [0 for i in range(n_visible)]
        for node in state.activities:
            if node.endswith("v"):
                activities[int(node[:-1])] = state.activities[node][0]
        visible_activities.append(activities)
    return visible_activities


if __name__ == '__main__':
    n_visible, n_hidden = 784, 200
    n_timesteps = 500
    np.random.seed(20230101)

    weights = read_weights("./weights.csv")
    v_biases = read_biases("./v_bias.csv", "v")
    h_biases = read_biases("./h_bias.csv", "h")

    visible_nodes = {"%sv" % n for n in range(n_visible)}
    hidden_nodes = {"%sh" % n for n in range(n_hidden)}

    network = ntm.topology.bipartite(set1=visible_nodes, set2=hidden_nodes,
                                     edge_attributes=weights)

    initial_conditions = initialize_rbm(visible_nodes, hidden_nodes, v_biases, h_biases)

    def activity_rule(ctx):
        node = ctx.node_label
        t = ctx.timestep
        activity, bias = ctx.current_activity

        # sampling with the RBM involves alternate sampling from the visible and hidden units
        if t % 2 == 0 and node in hidden_nodes:
            return activity, bias
        if t % 2 != 0 and node in visible_nodes:
            return activity, bias

        V = 0
        for neighbour_label in ctx.neighbour_labels:
            V += ctx.connection_states[neighbour_label][0]["weight"] * ctx.activities[neighbour_label][0]
        p = sigmoid(bias + V)

        return np.random.binomial(1, p), bias

    trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                            activity_rule=activity_rule, timesteps=n_timesteps)

    visible_activities = get_visible_activities(trajectory)

    ntm.animate_activities(visible_activities, shape=(28, 28), with_timestep=True, blit=False, interval=1)
