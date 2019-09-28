Netomaton
=========

Netomaton is a Python framework for exploring discrete dynamical network
systems, also known as Network Automata. It is a software abstraction
meant to aid in the implementation of models of collective computation.
Examples of such computational models include Cellular Automata and
Neural Networks.

### Getting Started

Netomaton can be installed via pip:

```
pip install netomaton
```

Requirements for using this library are Python 3.6, numpy 1.15.4,
matplotlib 3.0.2, and networkx 2.2.


### What are Network Automata?

The [Wikipedia entry](https://en.wikipedia.org/wiki/Network_automaton)
for Network Automata has stated:

> A network automaton (plural network automata) is a mathematical system consisting of a network of nodes that evolves over time according to predetermined rules. It is similar in concept to a cellular automaton, but much less studied.

> Stephen Wolfram's book _A New Kind of Science_, which is primarily concerned with cellular automata, briefly discusses network automata, and suggests (without positive evidence) that the universe might at the very lowest level be a network automaton.

A Network Automaton is a discrete dynamical system comprised of a collection
of nodes (the computational units) causally connected to eachother, as
specified by a network-defining adjacency matrix. The nodes adopt states
at each timestep of the network's evolution, as prescribed by an activity
function, *f*. Moreover, the network's topology can also change over time, as
prescribed by a connectivity function, *g*.

The network's topology is specified by the adjacency matrix, **A**, which
is of size _N_<sub>tot</sub> *X* _N_<sub>tot</sub>, where _N_<sub>tot</sub>
represents the total number of nodes in the network. Each non-zero entry
in **A** represents the existence of a link. The value of the entry
represents a link weight. The matrix **A** thus contains information
about the existence of links, and their direction.

The network is evolved for *T* timeteps. The activity of the network is
defined by the activities of all its nodes, and is represented by **S**<sub>*t*</sub>,
where *t* is a particular timestep. During each timestep, the activity
function *f* is invoked, followed by the connectivity function *g*, such
that:

**S**<sub>*t+1*</sub> = *f*(**A**<sub>*t*</sub>, **S**<sub>*t*</sub>)

**A**<sub>*t+1*</sub> = *g*(**A**<sub>*t*</sub>, **S**<sub>*t*</sub>)


A network may have nodes added or removed at any given timestep; however,
this framework will consider that a network has a total fixed number of
nodes at all times, and that nodes may become connected or fully
disconnected from the network instead.

To learn more, please refer to the scientific literature on the subject:

> Sayama, Hiroki, and Craig Laramee. "Generative network automata: A generalized framework for modeling adaptive network dynamics using graph rewritings." Adaptive Networks. Springer, Berlin, Heidelberg, 2009. 311-332.

> Smith, David MD, et al. "Network automata: Coupling structure and function in dynamic networks." Advances in Complex Systems 14.03 (2011): 317-339.

### Examples

Here's an example of the Elementary Cellular Automaton Rule 30 (as
described by Stephen Wolfram in his book
[_A New Kind of Science_](https://www.wolframscience.com/nks/)),
implemented with the Netomaton library:
```python
import netomaton as ntm

adjacency_matrix = ntm.network.cellular_automaton(n=200)

initial_conditions = [0] * 100 + [1] + [0] * 99

activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=100,
                           activity_rule=lambda ctx: ntm.rules.nks_ca_rule(ctx, 30))

ntm.plot_grid(activities)
```

<img src="resources/rule30.png" width="50%"/>

This repository contains examples of implementations of
various kinds of collective computation models, all implemented using
the Netomaton framework. Follow the link to learn more:

* [Elementary Cellular Automata](demos/elementary_ca/README.md)

* [1D Cellular Automata with Totalistic Rules](demos/totalistic_ca/README.md)

* [Reversible 1D Cellular Automata](demos/reversible_ca/README.md)

* [Density Classification with Evolved 1D Cellular Automata](demos/ca_density_classification/README.md)

* [Density Classification with a Watts-Strogatz small-world graph](demos/small_world_density_classification/README.md)

* [Asynchronous Automata](demos/asynchronous_automata/README.md)

* [Continuous Automata](demos/continuous_automata/README.md)

* [Finite State Machines](demos/finite_state_machine/README.md)

* [Pushdown Automata](demos/pushdown_automata/README.md)

* [Turing Machines](demos/turing_machine/README.md)

* [Langton's Lambda and Measures of Complexity](demos/langtons_lambda/README.md)

* [2D Cellular Automata](demos/totalistic_ca2d/README.md)

* [Conway's Game of Life](demos/game_of_life/README.md)

* [Gray-Scott Reaction-Diffusion Model](demos/reaction_diffusion/README.md)

* [Hexagonal Cell Lattices](demos/hexagonal_ca/README.md)

* [Hopfield Network](demos/hopfield_net/README.md)

* [Perturbations](demos/perturbation_demo/README.md)

* [Sandpiles](demos/sandpiles/README.md)

* [Continuous-Time Models](demos/continuous_time_models/README.md)

* [Travelling Salesman Problem with the Hopfield-Tank Neural Net](demos/hopfield_tank_tsp/README.md)

Additionally, this library includes a number of utility functions for
working with the results produced by the automata. For example, there
is the `animate` function, which is explained more [here](demos/animation_demo/README.md).
It is also important to understand the `timesteps` and `input`
parameters of the `evolve` function, explained [here](demos/timesteps_and_input/README.md).

### About this project

This project proposes the idea that many popular and well-known
collective computational models can all be thought of as Network Automata.
Such models include Cellular Automata, Boltzmann Machines, and various
flavours of Neural Networks, such as the Hopfield Net, and the Multilayer
Perceptron. This library does not attempt to be a replacement for great
frameworks such as TensorFlow, which are optimized, both in software and
hardware, for working with Neural Networks, for example. What this library
does attempt to be is a generalization of collective computation,
instantiated in software, with the goal of helping us see similarities
between models, and imagine new models that borrow features from existing
examples. It aims to provide a software architecture for understanding
and exploring the nature of computation in potentially dynamic networks.

Netomaton arose from a personal need to reconcile various models of collective
computation. In what fundamental ways does a Neural Network differ from a
Cellular Automaton? What can a Boltzmann Machine do that other models can't?
What do any of these models have in common? What sorts of new models can
we imagine? These are the questions that this library aspires to help answer.

Netomaton tries to make accessible any model of collective computation.
In so doing, it adopts certain generalizations and abstractions that,
while providing a common language for discussing seemingly disparate kinds of
models, incur a cost in terms of increased runtime complexity. The cost
of being very general is a less than ideal runtime performance, as any
given implementation is not optimized for a specific setting. For
example, regarding neural networks roughly as a series of matrix
multiplications allows one to take advantage of software and hardware
that can do those operations quickly. The focus of Netomaton, on the
other hand, is not on practicality, but on flexibility.

### Development

Create a Conda environment from the provided environment YAML file:
```
$ conda env create -f netomaton_dev.yaml
```

**Testing**

There are a number of unit tests for this project. To run the tests:
```
$ pytest tests
```
