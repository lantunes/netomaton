# Langton's Loops

In 1984, Christopher Langton described a type of 2-dimensional cellular automaton that exhibits a self-replicating 
dynamic loop structure. A branch of Artificial Life research developed from this work, resulting in better insight into 
self-replicating processes, which has obvious relevance to Biology and living systems. 

Below is an example of Langton's loop. This example makes use of the `LangtonsLoop` class, which is an extension of 
the `CTRBLRule` class, which can be used for constructing any kind of rule based on a von Neumann neighbourhood which 
considers the Center, Top, Right, Bottom and Left cells explicitly.

```python
import netomaton as ntm

dim = (75, 75)
rule = ntm.LangtonsLoop(dim=dim)

# the initial conditions consist of a single loop
initial_conditions = rule.init_loops(1, [40], [25])

trajectory = ntm.evolve(initial_conditions=initial_conditions,
                        network=rule.network, timesteps=500,
                        activity_rule=rule.activity_rule)

ntm.animate_activities(trajectory, shape=dim)
```

<img src="../../resources/langtons_loops.gif" width="100%"/>

The full source code can be found [here](langtons_loops_demo.py).

For more information, see:

> Langton, C. G. (1984). Self-reproduction in Cellular Automata. Physica D: Nonlinear Phenomena, 10(1-2), 135-144.

> https://en.wikipedia.org/wiki/Langton%27s_loops
