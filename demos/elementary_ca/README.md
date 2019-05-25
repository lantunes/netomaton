### Elementary Cellular Automata

This example demonstrates the Rule 30 Elementary Cellular Automaton. Currently, only 1- and 2-dimensional _k_-color
cellular automata with periodic boundary conditions are supported. The size of the neighbourhood can be adjusted. The
cellular automata produced by this library match the corresponding cellular automata available
at [atlas.wolfram.com](http://atlas.wolfram.com).

```python
from netomaton import *

adjacencies = AdjacencyMatrix.cellular_automaton(n=200)

initial_conditions = [0] * 100 + [1] + [0] * 99

activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=100,
                                    activity_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 30))

plot_grid(activities)
```

<img src="../../resources/rule30.png" width="50%"/>

The full source code for this example can be found [here](elementary_ca_demo.py).
