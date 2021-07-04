.. _contents:

Netomaton
=========

Netomaton is a tool for exploring discrete dynamical systems. This includes many models of computation, such as
Cellular Automata, and even Neural Networks. This also includes some continuous dynamical systems, such as ordinary
and partial differential equations, since the simulation of such systems involves the discretization of space and time.
Netomaton is also a tool for exploring Complex Systems.

Underlying all discrete dynamical systems (and discretized continuous dynamical systems) are networks of stateful units
that obey rules that specify how their states change over time. Netomaton thus considers all dynamical systems as
a model of computation known as Functional Network Automata.

- definition of FNA; references

Network Representations
-----------------------

The most general representation of the network underlying a system in Netomaton is the directed, weighted hypergraph.
However, in most cases, an adjacency matrix, which is also supported, will do. For large graphs, or when it is simply
more convenient, the network topology can be described with a connectivity map.

Adjacency Matrix
~~~~~~~~~~~~~~~~

- a matrix where each row indicates the outgoing links for a node

e.g. a->b->c::

      a  b  c
     --------
  a | 0  1  0
  b | 0  0  1
  c | 0  0  0

- example of random network
- code snippet of adjacency matrix
- show graph of network

- example of 1D ECA
- code snippet of adjacency matrix
- show graph of network

- helper functions for adjacency matrices

Network
~~~~~~~

- remember to use an OrderedMap if node iteration order is important when evolving the system
- actually, since we require Python 3.6, this is not strictly required, but it should be mentioned
- we should at least mention that the iteration order will reflect the dict insertion order, so one has to be aware of this

e.g. consider the following directed hypergraph (from https://en.wikipedia.org/wiki/Hypergraph)::

  V={1,2,3,4,5,6}
  E={a1,a2,a3,a4,a5}
   ={({1},{2}), ({2},{3}), ({3},{1}), ({2,3},{4,5}), ({3,5},{6})}.

.. code-block:: python

   n = ntm.Network()
   n.add_edge(1, 2, label="a1")
   n.add_edge(2, 3, label="a2")
   n.add_edge(3, 1, label="a3")
   n.add_edge(2, 4, label="a4")
   n.add_edge(3, 4, label="a4")
   n.add_edge(2, 5, label="a4")
   n.add_edge(3, 5, label="a4")
   n.add_edge(3, 6, label="a5")
   n.add_edge(5, 6, label="a5")


- in some cases, the edges are stateful as well as nodes

- only Python objects are allowed in the Network; no objects like NumPy numbers are allowed

Time Evolution
--------------

- a node's state is called its activity
- a network's activity is the state of all its nodes

- a link between two nodes is called a connection
- connections also have state, called the connection state

The Activity Rule
~~~~~~~~~~~~~~~~~

- the activity rule is optional

The Topology Rule
~~~~~~~~~~~~~~~~~

- the topology rule is optional

Update Order
~~~~~~~~~~~~

In the following, S represents the activities and A represents the topology:

activities-first
S(t + 1) = G(A(t), S(t))
A(t + 1) = F(A(t), S(t + 1))

topology-first
A(t + 1) = F(A(t), S(t))
S(t + 1) = G(A(t + 1), S(t))

synchronous:
A(t + 1) = F(A(t), S(t))
S(t + 1) = G(A(t), S(t))

Timesteps and Input
~~~~~~~~~~~~~~~~~~~
TODO

Initial and Past Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
TODO

Perturbations
~~~~~~~~~~~~~
TODO

Return Value
~~~~~~~~~~~~

The evolve() function returns a Trajectory, which is a list of States occupied by the system over time. A State is
comprised of the Network and its node Activities.

We maintain this dichotomy of a network and its activities for both conceptual and technical reasons.
While it is possible to combine the two, by having the network store the node activities, this is not aligned with
the existence of separate activity and topology rules. Moreover, having the activities separate from the network allows
for more control over the performance and memory usage during a simulation. For example, one may not care to keep track
of the network over time, and thus it becomes possible to carry only a single network through the time evolution of the
system when the activities are separate, since a new copy of the network needn't be created every timestep for the sake
of storing the new activities only.

Documentation
-------------

.. toctree::
   :maxdepth: 1

   reference
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
