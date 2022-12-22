# Fredkin's Self-Replicating Cellular Automata

Ed Fredkin described an interesting cellular automaton that exhibits self-replication. The CA is 2-dimensional, and 
can consist of two or more colors. To compute the state of a cell at the next timestep, one sums the states of the 
neighbouring cells, modulo _p_, where _p_ represents the number of colors. The neighborhood can be either of the Moore 
or von Neumann type. As the CA evolves, copies of the initial configuration will be produced. The examples below of 
these CA are based on John D. Cook's blog posts, 
[here](https://www.johndcook.com/blog/2021/05/03/self-reproducing-cellular-automata/) and 
[here](https://www.johndcook.com/blog/2021/05/03/multicolor-reproducing-ca/):

The following is an example of the Fredkin self-replicating CA with a von Neumann neighborhood:

```python
import netomaton as ntm
import numpy as np

network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='von Neumann')

initial_conditions = ntm.init_simple2d(60, 60)
# the letter "E"
initial_conditions[1709] = 1
initial_conditions[1710] = 1
initial_conditions[1711] = 1
initial_conditions[1769] = 1
initial_conditions[1829] = 1
initial_conditions[1830] = 1
initial_conditions[1831] = 1
initial_conditions[1889] = 1
initial_conditions[1949] = 1
initial_conditions[1950] = 1
initial_conditions[1951] = 1

def activity_rule(ctx):
    return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 2

trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=20,
                        activity_rule=activity_rule)

ntm.animate_activities(trajectory, shape=(60, 60), interval=350)
```

<img src="../../resources/fredkin_self_replicating_ca_vonneumann_demo.gif" width="50%"/>

The full source code for this example can be found [here](fredkin_self_replicating_ca_vonneumann_demo.py).

The following is an example of the Fredkin self-replicating CA with a Moore neighborhood:

```python
import netomaton as ntm
import numpy as np

network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')

initial_conditions = ntm.init_simple2d(60, 60)
# the letter "E"
initial_conditions[1709] = 1
initial_conditions[1710] = 1
initial_conditions[1711] = 1
initial_conditions[1769] = 1
initial_conditions[1829] = 1
initial_conditions[1830] = 1
initial_conditions[1831] = 1
initial_conditions[1889] = 1
initial_conditions[1949] = 1
initial_conditions[1950] = 1
initial_conditions[1951] = 1

def activity_rule(ctx):
    return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 2

trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=20,
                        activity_rule=activity_rule)

ntm.animate_activities(trajectory, shape=(60, 60), interval=350)
```

<img src="../../resources/fredkin_self_replicating_ca_moore_demo.gif" width="50%"/>

The full source code for this example can be found [here](fredkin_self_replicating_ca_moore_demo.py).

The following is an example of the Fredkin self-replicating multi-color CA with a von Neumann neighborhood:

```python
import netomaton as ntm
import numpy as np

network = ntm.topology.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='von Neumann')

initial_conditions = ntm.init_simple2d(60, 60)
# the letter "E"
initial_conditions[1709] = 0
initial_conditions[1710] = 1
initial_conditions[1711] = 2
initial_conditions[1769] = 3
initial_conditions[1829] = 4
initial_conditions[1830] = 5
initial_conditions[1831] = 6
initial_conditions[1889] = 7
initial_conditions[1949] = 8
initial_conditions[1950] = 9
initial_conditions[1951] = 10

def activity_rule(ctx):
    return (np.sum(ctx.neighbourhood_activities) - ctx.current_activity) % 11

trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=23,
                        activity_rule=activity_rule)

ntm.animate_activities(trajectory, shape=(60, 60), interval=350, colormap='viridis')
```

<img src="../../resources/fredkin_self_replicating_ca_multicolor_demo.gif" width="50%"/>

The full source code for this example can be found [here](fredkin_self_replicating_ca_multicolor_demo.py).

For more information, see:

> Edwin R. Banks, Information Processing and Transmission in Cellular Automata. MIT dissertation. January 1971.

> https://www.johndcook.com/blog/2021/05/03/self-reproducing-cellular-automata/

> https://www.johndcook.com/blog/2021/05/03/multicolor-reproducing-ca/
