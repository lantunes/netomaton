import netomaton as ntm
import numpy as np
import csv
import matplotlib.pyplot as plt


def read_weights(fname):
    weights = {}
    with open(fname, "rt") as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            node2 = i
            for j, weight in enumerate(line):
                node1 = j
                if node1 not in weights:
                    weights[node1] = {}
                weights[node1][node2] = float(weight)
    return weights


def read_image_activities(fname):
    activities = {}
    with open(fname, "rt") as f:
        reader = csv.reader(f)
        node_label = 0
        for line in reader:
            for activity in line:
                activities[node_label] = float(activity)
                node_label += 1
    return activities


def set_weights(network, weights):
    for i in weights:
        for j in weights[i]:
            network.update_edge(i, j, weight=weights[i][j])


def relu(x):
    return x if x > 0 else 0


def identity(x):
    return x


def softmax(x):
    e = np.exp(x)
    return e / np.sum(e)


"""
MLP architecture:

layer 1: 784 neurons (input layer)
         [layer1-2 weights]
layer 2: 784 neurons (1st hidden layer, ReLU)
         [layer2-3 weights]
layer 3: 784 neurons (2nd hidden layer, ReLU)
         [layer3-4 weights]
layer 4: 10 neurons (output layer, identity)
         [log softmax]
"""
if __name__ == '__main__':
    n_neurons = 784
    n_timesteps = 4  # one for each "layer"

    initial_conditions = read_image_activities("./mnist-class3.csv")

    # read the weights into memory; this MLP consists only of weights and no biases
    initial_weights = read_weights("./mlp_layer1-2_weights.csv")
    timestep_to_weights = {
        1: read_weights("./mlp_layer2-3_weights.csv"),
        2: read_weights("./mlp_layer3-4_weights.csv"),
        3: {}
    }

    timestep_to_activation = {
        1: relu,
        2: relu,
        3: identity
    }

    network = ntm.Network()
    # the network is fully connected, with an edge from each neuron
    #  to every other, including itself
    [network.add_edge(i, j) for i in range(n_neurons) for j in range(n_neurons)]
    set_weights(network, initial_weights)


    def activity_rule(ctx):
        V = 0
        for neighbour_label in ctx.neighbour_labels:
            V += ctx.connection_states[neighbour_label][0]["weight"] * ctx.activities[neighbour_label]
        activity = timestep_to_activation[ctx.timestep](V)
        return activity


    def topology_rule(ctx):
        curr_network = ctx.network
        new_weights = timestep_to_weights[ctx.timestep]
        set_weights(curr_network, new_weights)
        return curr_network


    trajectory = ntm.evolve(network, initial_conditions=initial_conditions, activity_rule=activity_rule,
                            topology_rule=topology_rule, update_order=ntm.UpdateOrder.ACTIVITIES_FIRST,
                            timesteps=n_timesteps)

    # at the end, nodes 0-9 will contain the values for the log softmax
    vals = [trajectory[-1].activities[i] for i in range(10)]

    plt.title("predicted class: %s" % np.argmax(np.log(softmax(vals))))
    plt.imshow(np.array([initial_conditions[i] for i in range(n_neurons)]).reshape((28, 28)), cmap="gray_r")
    plt.show()
