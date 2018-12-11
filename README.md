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

This repository contains examples of implementations of
various kinds of collective computation models, all implemented using
the Netomaton framework. Follow the link to see the source code:

* [Density Classification with a Watts-Strogatz small-world graph](https://github.com/lantunes/netomaton/blob/master/demos/small_world_density_classification_demo.py)

* [1D Cellular Automaton with Totalistic Rule 777](https://github.com/lantunes/netomaton/blob/master/demos/totalistic_ca_demo.py)
