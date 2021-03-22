Netomaton
=========

Netomaton is a tool for exploring discrete dynamical systems. This includes many models of computation, such as 
Cellular Automata, and even Neural Networks. This also includes some continuous dynamical systems, such as ordinary 
and partial differential equations, since the simulation of such systems involves the discretization of space and time.

Underlying all discrete dynamical systems (and discretized continuous dynamical systems) are networks of stateful units
that obey rules that specify how their states change over time. Netomaton thus considers all dynamical systems as 
a model of computation known as Functional Network Automata.

- definition of FNA; references

-------------

# Network Representations

The most general representation of the network underlying a system in Netomaton is the directed, weighted hypergraph. 
However, in most cases, an adjacency matrix, which is also supported, will do. For large graphs, or when it is simply 
more convenient, the network topology can be described with a connectivity map.

## Adjacency Matrix

- a matrix where each row indicates the outgoing links for a node
e.g. a->b->c
    a  b  c
  ---------
a | 0  1  0
b | 0  0  1
c | 0  0  0

- example of random network
-- code snippet of adjacency matrix
-- show graph of network

- example of 1D ECA
-- code snippet of adjacency matrix
-- show graph of network

- helper functions for adjacency matrices

## Hypergraph and Connectivity Map

- a map of maps, where each entry specified the incoming links for a node
e.g. a->b->c
{
  "a": {"a": 1.0}
  "b": {"a": 1.0, "b": 1.0}
  "c": {"b": 1.0, "c": 1.0}
}
- the edge weights are the same for all connections (1.0 in this case)

- remember to use an OrderedMap if node iteration order is important when evolving the system
-- actually, since we require Python 3.6, this is not strictly required, but it should be mentioned
-- we should at least mention that the iteration order will reflect the dict insertion order, so one has to be aware of this

- how would we represent a (directed, weighted) hypergraph?
- the value includes both the edge weight and its ID, as a 2-tuple (the edge ID can be any object, e.g. int, str)
e.g. consider the following hypergraph (from https://en.wikipedia.org/wiki/Hypergraph):

V={1,2,3,4,5,6} 
E={a1,a2,a3,a4,a5}
 ={({1},{2}), ({2},{3}), ({3},{1}), ({2,3},{4,5}), ({3,5},{6})}.

{
  1: {3: (1.0, "a3")},
  2: {1: (1.0, "a1")},
  3: {2: (1.0, "a2")},
  4: {2: (1.0, "a4"), 3: (1.0, "a4")},
  5: {2: (1.0, "a4"), 3: (1.0, "a4")},
  6: {3: (1.0, "a5"), 5: (1.0, "a5")}
}
- the weights are the same for all connections (1.0 in this case)

- how do we represent multi-edges? i.e. multiple edges from the same start and end node?

-- the value of an incoming connection in the connectivity map is model-specific
-- in the case of an ECA it could be anything (i.e. 1.0, "", it doesn't matter); in the case of a Hopfield net it is
   a single number, the edge weight; in the case of the Wolfram Physics model it is a tuple: the multiplicity of the 
   edge (i.e. for multi-edges) and the ID of the hyperedge the edge belongs to
-- this implies that, in some cases, the edges are stateful as well as nodes

# Time Evolution

## The Activity Rule

## The Connectivity Rule

## Timesteps and Input

## Initial and Past Conditions

## Perturbations

## Parallel Execution

- activity rule must not be stateful
- can the connectivity rule be supported?