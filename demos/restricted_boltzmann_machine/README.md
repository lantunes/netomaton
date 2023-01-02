# Restricted Boltzmann Machine

The Restricted Boltzmann Machine (RBM) is a stochastic neural network that is often used in machine learning tasks, such 
as classification and generative modelling. The original Boltzmann Machine can be thought of as a stochastic version 
of a Hopfield Network, with the novel element of consisting of separate "visible" and "hidden" units. The RBM further 
introduces the constraint that connections can only exist between visible and hidden units, and not between units of the 
same type. The resulting network thus adopts a bipartite graph topology.

Training an RBM aims to identify the best weights and biases for a task, and typically involves the use of the 
Contrastive Divergence procedure. Here, we don't include the means to train an RBM, but rather, we begin with a 
pre-trained network, and demonstrate the dynamical nature of the system by sampling an MNIST (handwritten character) 
image, beginning from a random input, using the Netomaton framework.

In the demo below, we construct an RBM with the Netomaton framework by creating a network with a bipartite topology, 
consisting of 784 visible nodes and 200 hidden nodes. The weights and biases were obtained externally. Each node's 
state consists of a binary (i.e. {1, 0}) activity and a (pre-trained) bias. To sample from the RBM, we initialize the 
"visible" nodes with binary activities chosen at random, and we set the activities of the "hidden" nodes to 0. We supply
an `activity_rule` that determines the state of a node at the next timestep. A node's activity is determined by drawing 
from a Bernoulli distribution parameterized with a probability based on the activities (and weights) of its 
neighbourhood. A special aspect of the RBM is that the visible and hidden nodes are updated in alternating fashion, such 
that on any given timestep either the visible nodes are updated while the hidden nodes are unchanged, or vice versa. _*_

```python
import netomaton as ntm
import numpy as np

n_visible, n_hidden = 784, 200
n_timesteps = 500

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
```

After evolving the network automaton for 500 timesteps, the system begins to approach an equilibrium state, and the 
visible nodes collectively begin to represent a discernible image of a handwritten character (perhaps a "5", or an "8"). 

<img src="../../resources/rbm.gif" width="50%"/>

The full source code for this example can be found [here](rbm_demo.py).

_*_ _NOTE: The RBM implemented here is for demonstration purposes only, to illustrate how an RBM fits within the 
framework of network automata. In practice, one wouldn't implement an RBM this way. Other frameworks, such as Tensorflow
and PyTorch, are much better suited for building practical implementations of RBM models._ 

For more information, please refer to the following resources:

> Hinton, G. E. (2002). Training products of experts by minimizing contrastive divergence. Neural Computation, 14(8), 
1771-1800.

> Hinton, G. E., & Salakhutdinov, R. R. (2006). Reducing the dimensionality of data with neural networks. Science, 
313(5786), 504-507.
