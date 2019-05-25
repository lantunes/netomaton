### 2D Cellular Automata

Netomaton supports 2-dimensional cellular automata with periodic
boundary conditions. The number of states, k, can be any whole number.
The neighbourhood radius, r, can also be any whole number, and both
Moore and von Neumann neighbourhood types are supported. The following
snippet demonstrates creating a 2D totalistic cellular automaton:

```python
import netomaton as ntm

adjacencies = ntm.AdjacencyMatrix.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')

initial_conditions = ntm.init_simple2d(60, 60)

activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=30,
                           activity_rule=lambda n, c, t: ntm.ActivityRule.totalistic_ca(n, k=2, rule=126))

ntm.plot_grid(activities, shape=(60, 60))
```

The full source code can be found [here](totalistic_2d_demo.py).

<img src="../../resources/rule126.gif" width="65%"/>
