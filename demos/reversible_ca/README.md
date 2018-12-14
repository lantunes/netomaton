### Reversible 1D Cellular Automata

Network automata can be explicitly made to be reversible. The following example demonstrates the
creation of the elementary reversible cellular automaton rule 90R:

```python
from netomaton import *

adjacencies = AdjacencyMatrix.cellular_automaton(n=200)

initial_conditions = np.random.randint(0, 2, 200)

r = ReversibleRule(lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 90))

activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=100,
                                    activity_rule=r.activity_rule)

plot_grid(activities)
```

<img src="https://raw.githubusercontent.com/lantunes/netomaton/master/resources/rule90R.png" width="50%"/>

The full source code for this example can be found [here](https://github.com/lantunes/netomaton/blob/master/demos/reversible_ca/reversible_ca_demo.py).
