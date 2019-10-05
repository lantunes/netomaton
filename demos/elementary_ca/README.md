# Elementary Cellular Automata

This example demonstrates the Rule 30 Elementary Cellular Automaton. Currently, only 1- and 2-dimensional _k_-color
Cellular Automata with periodic boundary conditions are supported. The size of the neighbourhood can be adjusted. The
Cellular Automata produced by this library match the corresponding Cellular Automata available
at [atlas.wolfram.com](http://atlas.wolfram.com).

```python
import netomaton as ntm

adjacency_matrix = ntm.network.cellular_automaton(n=200)

initial_conditions = [0] * 100 + [1] + [0] * 99

activities, adjacencies = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=100,
                                     activity_rule=lambda ctx: ntm.rules.nks_ca_rule(ctx, 30))

ntm.plot_grid(activities)
```

<img src="../../resources/rule30.png" width="50%"/>

The full source code for this example can be found [here](elementary_ca_demo.py).
