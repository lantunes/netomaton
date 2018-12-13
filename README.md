Netomaton
=========

Netomaton is a Python framework for exploring discrete dynamical network
systems, also known as Network Automata. It is a software abstraction
meant to aid in the implementation of models of collective computation.

This library proposes the idea that many popular and well-known
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

### What are Network Automata?

A Network Automaton is a discrete dynamical system comprised of a collection
of cells (the computational units) causally connected to eachother, as
specified by a network-defining adjacency matrix. The cells adopt states
at each timestep of the network's evolution, as prescribed by an activity
function, *f*. Moreover, the network's topology can also change over time, as
prescribed by a connectivity function, *g*.

The network's topology is specified by the adjacency matrix, **A**, which
is of size _N_<sub>tot</sub> *X* _N_<sub>tot</sub>, where _N_<sub>tot</sub>
represents the total number of nodes (i.e. cells) in the network. Each
non-zero entry in **A** represents the existence of a link. The value of
the entry represents a weight. The matrix **A** contains information about
the existence of links, and their direction.

The network is evolved for *T* timeteps. The activity of the network is
defined by the activities of all its nodes, and is represented by **S**<sub>*t*</sub>,
where *t* is a particular timestep. During each timestep, the activity
function *f* is invoked, followed by the connectivity function *g*, such
that:

**S**<sub>*t+1*</sub> = *f*(**A**<sub>*t*</sub>, **S**<sub>*t*</sub>)

**A**<sub>*t+1*</sub> = *g*(**A**<sub>*t*</sub>, **S**<sub>*t*</sub>)


A network may have nodes added or removed at any given timestep, however,
this framework will consider that a network has a total fixed number of
nodes at all times, and that nodes may become connected or fully
disconnected from the network instead.

### Examples

This repository contains examples of implementations of
various kinds of collective computation models, all implemented using
the Netomaton framework. Follow the link to see the source code:

* [Elementary Cellular Automaton Rule 30](https://github.com/lantunes/netomaton/blob/master/demos/elementary_ca)

* [1D Cellular Automaton with Totalistic Rule 777](https://github.com/lantunes/netomaton/blob/master/demos/totalistic_ca)

* [Density Classification with a Watts-Strogatz small-world graph](https://github.com/lantunes/netomaton/blob/master/demos/small_world_density_classification)

* [Hopfield Network](https://github.com/lantunes/netomaton/blob/master/demos/hopfield_net)
