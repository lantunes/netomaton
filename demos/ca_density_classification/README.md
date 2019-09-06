### Density Classification with Evolved 1D Cellular Automata

When creating a 1D cellular automaton adjacency matrix, the size of the
cell neighbourhood can be varied by setting the parameter _*r*_. The
value of _*r*_ represents the number of cells to the left and to the
right of the cell under consideration. Thus, to get a neighbourhood
size of 3, _*r*_ should be 1, and to get a neighbourhood size of 7,
_*r*_ should be 3.

As an example, consider the work of M. Mitchell et al., carried out in
the 1990s, involving the creation (discovery) of a cellular automaton
that solves the density classification problem: if the initial random
binary vector contains more than 50% of 1s, then a cellular automaton
that solves this problem will give rise to a vector that contains only
1s after a fixed number of time steps, and likewise for the case of 0s.
A very effective cellular automaton that solves this problem most of
the time was found using a Genetic Algorithm.

```python
import netomaton as ntm
import numpy as np

# set r to 3, for a neighbourhood size of 7
adjacencies = ntm.network.cellular_automaton(149, r=3)

initial_conditions = np.random.randint(0, 2, 149)

# Mitchell et al. discovered this rule using a Genetic Algorithm
rule_number = 6667021275756174439087127638698866559

print("density of 1s: %s" % (np.count_nonzero(initial_conditions) / 149))

activities, connectivities = ntm.evolve(initial_conditions, adjacencies, timesteps=149,
                                        activity_rule=lambda n, c, t: ntm.ActivityRule.binary_ca_rule(n, c, rule_number))

ntm.plot_grid(activities)
```
<img src="../../resources/density_classification.png" width="50%"/>

The full source code for this example can be found [here](ca_density_classification_demo.py).

For more information, see:

> Melanie Mitchell, James P. Crutchfield, and Rajarshi Das, "Evolving Cellular Automata with Genetic Algorithms: A Review of Recent Work", In Proceedings of the First International Conference on Evolutionary Computation and Its Applications (EvCA'96), Russian Academy of Sciences (1996).
