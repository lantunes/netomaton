# Hexagonal Cell Lattices

Netomaton supports automata with hexagonal node lattices. A hexagonal
node with a neighbourhood of radius 1 is depicted below:

<img src="../../resources/hexagon.png" width="40%"/>

The example below demonstrates the "snowflake" Cellular Automaton,
described on [page 371](https://www.wolframscience.com/nks/p371--the-growth-of-crystals/)
of Wolfram's *A New Kind of Science*:

```python
import netomaton as ntm

adjacency_matrix = ntm.topology.adjacency.cellular_automaton2d(60, 60, r=1, neighbourhood="Hex")

initial_conditions = ntm.init_simple2d(60, 60)

activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=31,
                           activity_rule=lambda ctx: 1 if sum(ctx.activities) == 1 else ctx.current_activity)

ntm.animate_hex(activities, shape=(60, 60), interval=150)
```

<img src="../../resources/snowflake.gif" width="40%"/>

The full source code for this example can be found [here](hexagonal_ca_demo.py).
