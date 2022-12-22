<div align="center">
<img src="https://raw.githubusercontent.com/lantunes/netomaton/master/resources/logo.png" alt="logo"></img>
</div>

<b>Netomaton</b> is a Python framework for exploring discrete dynamical systems. It is a software abstraction
meant to aid in the implementation of models of collective computation. Examples of such computational models include 
Cellular Automata and Neural Networks. This also includes some continuous dynamical systems, such as ordinary and 
partial differential equations, since the simulation of such systems involves the discretization of space and time. 
Netomaton is also a tool for exploring Complex Systems.

Underlying all discrete dynamical systems (and discretized continuous dynamical systems) are networks of stateful units 
that obey rules that specify how their states change over time. Netomaton thus considers all dynamical systems as a 
model of computation known as Functional Network Automata.

[![testing status](https://github.com/lantunes/netomaton/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/lantunes/netomaton/actions)
[![latest version](https://img.shields.io/pypi/v/netomaton?style=flat-square&logo=PyPi&logoColor=white&color=blue)](https://pypi.org/project/netomaton/)

### Getting Started

Netomaton can be installed via pip:

```
pip install netomaton
```

Requirements for using this library are Python 3.6, numpy 1.15.4,
matplotlib 3.0.2, networkx 2.5, and msgpack 1.0.2.


### What are Network Automata?

The [Wikipedia entry](https://en.wikipedia.org/wiki/Network_automaton)
for Network Automata has stated:

> A network automaton (plural network automata) is a mathematical system consisting of a network of nodes that evolves over time according to predetermined rules. It is similar in concept to a cellular automaton, but much less studied.

> Stephen Wolfram's book _A New Kind of Science_, which is primarily concerned with cellular automata, briefly discusses network automata, and suggests (without positive evidence) that the universe might at the very lowest level be a network automaton.

A Network Automaton is a discrete dynamical system comprised of a collection
of nodes (the computational units) causally connected to each other, as
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

The network is evolved for *T* timesteps. The activity of the network is
defined by the activities of all its nodes, and is represented by **S**<sub>*t*</sub>,
where *t* is a particular timestep. During each timestep, the activity
function *f* is invoked, followed by the connectivity function *g*, such
that:

**S**<sub>*t+1*</sub> = *f*(**A**<sub>*t*</sub>, **S**<sub>*t*</sub>)

**A**<sub>*t+1*</sub> = *g*(**A**<sub>*t*</sub>, **S**<sub>*t*</sub>)


There are no restrictions to the kinds of topological changes that a
network may undergo over the course of its evolution. A network may have
nodes added or removed at any given timestep.

To learn more, please refer to the scientific literature on the subject:

> Wolfram, S. (2002). A New Kind of Science (pp. 475–545). Champaign, IL: Wolfram Media.

> Tomassini, Marco. "Generalized automata networks." International Conference on Cellular Automata. Springer, Berlin, Heidelberg, 2006.

> Sayama, Hiroki, and Craig Laramee. "Generative network automata: A generalized framework for modeling adaptive network dynamics using graph rewritings." Adaptive Networks. Springer, Berlin, Heidelberg, 2009. 311-332.

> Smith, David MD, et al. "Network automata: Coupling structure and function in dynamic networks." Advances in Complex Systems 14.03 (2011): 317-339.

### Examples

Here's an example of the Elementary Cellular Automaton Rule 30 (as
described by Stephen Wolfram in his book
[_A New Kind of Science_](https://www.wolframscience.com/nks/)),
implemented with the Netomaton library:
```python
import netomaton as ntm

network = ntm.topology.cellular_automaton(n=200)

initial_conditions = [0] * 100 + [1] + [0] * 99

trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions,
                        activity_rule=ntm.rules.nks_ca_rule(30), timesteps=100,
                        memoize=True)

ntm.plot_activities(trajectory)
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
* [Fredkin's Self-Replicating CA](demos/fredkin_self_replicating_ca/README.md)
* [Langton's Loops](demos/langtons_loops/README.md)
* [Gray-Scott Reaction-Diffusion Model](demos/reaction_diffusion/README.md)
* [Hexagonal Cell Lattices](demos/hexagonal_ca/README.md)
* [Hopfield Network](demos/hopfield_net/README.md)
* [Perturbations](demos/perturbation_demo/README.md)
* [Sandpiles](demos/sandpiles/README.md)
* [Continuous-Time Models](demos/continuous_time_models/README.md)
* [Travelling Salesman Problem with the Hopfield-Tank Neural Net](demos/hopfield_tank_tsp/README.md)
* [Logistic Map](demos/logistic_map/README.md)
* [Collatz Conjecture](demos/collatz_conjecture/README.md)
* [Substitution Systems](demos/substitution_systems/README.md)
* [Lindenmayer Systems](demos/lindenmayer_systems/README.md)
* [Wireworld](demos/wireworld/README.md)
* [Random Attachment Model](demos/random_attachment_model/README.md)
* [Randomly Growing Network](demos/randomly_growing_network/README.md)
* [Restricted Network Automata](demos/restricted_network_automata/README.md)
* [Fungal Growth Model](demos/fungal_growth/README.md)
* [Wolfram Physics Model](demos/wolfram_physics/README.md)

Additionally, this library includes a number of utility functions for
working with the results produced by the automata. For example, there
is the `animate` function, which is explained more [here](demos/animation_demo/README.md).
It is also important to understand the `timesteps` and `input`
parameters of the `evolve` function, explained [here](demos/timesteps_and_input/README.md).

### About this project

This project proposes the idea that many popular and well-known
collective computational models can all be thought of as Functional Network Automata.
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

**Documentation**

To build the Sphinx documentation, from the `doc` directory:
```
$ make clean html
```
The generated files will be in `_build/html`.

**Testing**

There are a number of unit tests for this project. To run the tests:
```
$ pytest tests
```

--------------------

### Citation Info

This project has been published on [Zenodo](https://zenodo.org/record/3893141#.XuUOg55KhZI),
which provides a DOI, as well as an easy way to generate citations in a number of formats.
For example, this project may be cited as:


> Antunes, Luis M. (2019, September 28). Netomaton: A Python Library for working with 
Network Automata. Zenodo. http://doi.org/10.5281/zenodo.3893141


BibTeX:
```
@software{antunes_luis_m_2019_3893141,
  author       = {Antunes, Luis M.},
  title        = {{Netomaton: A Python Library for working with 
                   Network Automata}},
  month        = sep,
  year         = 2019,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.3893141},
  url          = {https://doi.org/10.5281/zenodo.3893141}
}
```

### Stars

Please star this repository if you find it useful, or use it as part of your research.

### Copyrights

Copyright (c) 2018-2020 Luis M. Antunes (@lantunes) All rights reserved.
