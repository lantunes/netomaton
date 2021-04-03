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

e.g.: [(1,2),(1,2,3,1,2),(4,3),(4,3),(5,4)]  //Wolfram Model configuration

{
	1: {
		3: [                      // items in the array represent multplicity; e.g. there is one connection from 3 to 1 here
			{
				"label": "1",
				"hyperedge": {
					"index": 2
				}
			}
		]
	},
	2: {
		1: [                      // there are two connections from 1 to 2 here
			{
				"label": "1",     //optional, but required if hyperedge; string; the label identifying the edge
				"weight": 1.0,    //optional
				"unary": false,   //optional, false by default; if true, the incoming node must match the node receiving the connection
				"hyperedge": {    //optional; hyperedge metadata
					"index": 0       //optional; indicates the position in the n-ary relation
				}
			},
			{
				"weight": 1.0,
			},
			{
				"label": "1",
				"hyperedge": {
					"index": 3
				}
			}
		]
	},
	3: {
		2: [
			{
				"label": "1",
				"hyperedge": {
					"index": 1
				}
			}
		],
		4: [{}, {}]               // there are two edges from 4 to 3
	},
	4: {
		5: [{}]                   // there is one edge from 5 to 4
	},
	5: {}                         // 5 has no incoming connections
}


e.g. consider the following directed hypergraph (from https://en.wikipedia.org/wiki/Hypergraph):

V={1,2,3,4,5,6} 
E={a1,a2,a3,a4,a5}
 ={({1},{2}), ({2},{3}), ({3},{1}), ({2,3},{4,5}), ({3,5},{6})}.

{
  1: {
  	3: [{
  		"label": "a3"
  	}]
  },
  2: {
  	1: [{
  		"label": "a1"
  	}]
  },
  3: {
  	2: [{
  		"label": "a2"
  	}]
  },
  4: {
  	2: [
  		{
  			"label": "a4"
  			"hyperedge": {}  // the label is enough to indicate a hyperedge in this case
  		}
  	],
  	3: [
  		{
  			"label": "a4"
  			"hyperedge": {}	
  		}
  	]
  },
  5: {
  	2: [
  		{
  			"label": "a4"
  			"hyperedge": {}
  		}
  	],
  	3: [
  		{
  			"label": "a4"
  			"hyperedge": {}	
  		}
  	]
  },
  6: {
  	3: [
  		{
  			"label": "a5"
  			"hyperedge": {}	
  		}
  	], 
  	5: [
  		{
  			"label": "a5"
  			"hyperedge": {}	
  		}
  	]
  }
}

The connectivity map provides a list of all the nodes in the network.
- for each node, it lists all the incoming nodes, and the states of those connections

-- the value of an incoming connection in the connectivity map is model-specific
-- in the case of an ECA it could be anything (i.e. 1.0, "", it doesn't matter); in the case of a Hopfield net it is
   a single number, the edge weight; in the case of the Wolfram Physics model it is a tuple: the multiplicity of the 
   edge (i.e. for multi-edges) and the ID of the hyperedge the edge belongs to
-- this implies that, in some cases, the edges are stateful as well as nodes

# Time Evolution

- a node's state is called its activity
-- a network's activity is the state of all its nodes

- a link between two nodes is called a connection
-- connections also have state, called the connection state

## The Activity Rule

- the activity rule is optional

## The Connectivity Rule

TODO rename to Topology Rule

- the connectivity rule is optional

## Timesteps and Input

## Initial and Past Conditions

## Perturbations
