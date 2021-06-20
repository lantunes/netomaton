# Wolfram Physics Model

The [Wolfram Physics Project](https://www.wolframphysics.org/) aims to find the fundamental theory of Physics. 
Underlying the proposed model is an evolving hypergraph, from which all observable phenomena emerges.

The Netomaton project contains an implementation of the Wolfram Physics model. An example of usage of the model is
given below:

```python
import netomaton as ntm
from netomaton.vis import show_network

# wm1167
rules = {
    "in": [(1, 1, 2), (3, 4, 1)], "out": [(1, 1, 4), (5, 4, 3), (2, 5, 1)]
}
config = [(1, 1, 1), (1, 1, 1)]

model = ntm.WolframPhysicsModel(config, rules)

trajectory = ntm.evolve(network=model.network, topology_rule=model.topology_rule, timesteps=198)

show_network(trajectory[-1].network)
```

<img src="../../resources/wolfram_physics.gif" width="40%"/>

Note that `show_network` will launch a browser. The full source code for this example can be found 
[here](wolfram_physics_demo.py).

For more information about the Wolfram Physics Project, see:

> Wolfram, S. (2020). A Project to Find the Fundamental Theory of Physics. Wolfram Media.
