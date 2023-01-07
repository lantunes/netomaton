# Multilayer Perceptron

A Multilayer Perceptron (MLP) is a feed-forward neural network that is used for classification and regression tasks. The
MLP consists of a number of layers of neurons, whose activities are determined from the incoming activities of neurons 
in the preceding layer. The weights of the connections between neurons are discovered using the backpropagation training
procedure.

Here, we demonstrate that an MLP can be thought of as a discrete dynamical system. Normally, the network consists of a 
number of layers of neurons, connected in a feed-forward topology. The activities of a layer can only be computed once 
the activities of the preceding layer are computed. However, we can consider that each layer actually represents a 
timestep in the dynamical evolution of a fixed set of neurons that are fully connected to each other. (In an MLP, there 
can be a variable number of neurons per layer, and this is still compatible with the dynamical system view. However, for 
simplicity, here we'll assume that each layer contains the same number of neurons.) In such a dynamical system view, the 
network is updated at each timestep so that it contains the appropriate set of weights. Thus, for an MLP with 4 layers 
(i.e. an input later, 2 hidden layers, and an output layer), we can imagine that first layer of neurons evolving for 4 
timesteps, replacing the weights of the fully connected network (including self-connections) at each timestep.

The code snippet below illustrates this idea with the Netomaton framework:

```python
import netomaton as ntm
import numpy as np
import matplotlib.pyplot as plt

n_neurons = 784
n_timesteps = 4  # one for each "layer"

initial_conditions = read_image_activities("./mnist-class3.csv")

# read the weights into memory; this MLP consists only of weights and no biases
initial_weights = read_weights("./mlp_layer1-2_weights.csv")
# a map from the timestep to which weights to use at that timestep
timestep_to_weights = {
    1: read_weights("./mlp_layer2-3_weights.csv"),
    2: read_weights("./mlp_layer3-4_weights.csv"),
    3: {}
}

# a map from the timestep to which activation function to use that timestep
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
```

In the example above, we create a fully-connected directed network (with self-connections) consisting of 784 neurons. 
Each neuron corresponds to a pixel in an MNIST image. The neurons are initialized with an image (the handwritten 
character 3 in this example). The weights were obtained externally (there are no biases in this example).  We evolve 
the network for 4 timesteps, replacing the weights of the network at each timestep. At the end, we obtain the activities
of the first 10 neurons only, which contain the inputs for the log-softmax function, which will be used to obtain the 
index of the neuron corresponding to the class with the highest estimated log probability. Finally, we plot the image 
and the system's prediction. _*_

<img src="../../resources/mlp_class3.png" width="30%"/>

The full source code for this example can be found [here](mlp_demo.py).

_*_ _NOTE: The MLP implemented here is for demonstration purposes only, to illustrate how an MLP fits within the 
framework of network automata. In practice, one wouldn't implement an MLP this way. Other frameworks, such as Tensorflow
and PyTorch, are much better suited for building practical implementations of MLP models._

For more information, please refer to the following resources:

https://en.wikipedia.org/wiki/Multilayer_perceptron
