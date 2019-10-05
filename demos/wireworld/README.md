### Wireworld

Wireworld is a Turing-complete Cellular Automaton, first described by
Brian Silverman in 1987. Wireworld can be used to simulate electronic
gates, or logic elements.

An example of Wireworld diodes is given below:
```python
import netomaton as ntm
from matplotlib.colors import ListedColormap

adjacency_matrix = ntm.network.cellular_automaton2d(rows=13, cols=14, neighbourhood="Moore")

initial_conditions = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
    2, 1, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3,
    0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
    2, 1, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3,
    0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

def wireworld(ctx):
    if ctx.current_activity == 0:  # empty
        return 0
    if ctx.current_activity == 1:  # electron head
        return 2
    if ctx.current_activity == 2:  # electron tail
        return 3
    if ctx.current_activity == 3:  # conductor
        electron_head_count = ctx.activities.count(1)
        return 1 if electron_head_count == 1 or electron_head_count == 2 else 3

activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, activity_rule=wireworld, timesteps=15)

ntm.animate(activities, shape=(13, 14), interval=120, show_grid=True,
            colormap=ListedColormap(["black", "blue", "red", "yellow"]))
```
<img src="../../resources/wireworld_diodes.gif" width="50%"/>

The full source code for this example can be found [here](wireworld_diodes_demo.py).

An exmaple of a Wireworld XOR gate is given below:
```python
import netomaton as ntm
from matplotlib.colors import ListedColormap

adjacency_matrix = ntm.network.cellular_automaton2d(rows=13, cols=24, neighbourhood="Moore")

initial_conditions = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 1, 2, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 3, 3, 3, 2,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 2, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,
    0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

def wireworld(ctx):
    if ctx.current_activity == 0:  # empty
        return 0
    if ctx.current_activity == 1:  # electron head
        return 2
    if ctx.current_activity == 2:  # electron tail
        return 3
    if ctx.current_activity == 3:  # conductor
        electron_head_count = ctx.activities.count(1)
        return 1 if electron_head_count == 1 or electron_head_count == 2 else 3

activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, activity_rule=wireworld, timesteps=25)

ntm.animate(activities, shape=(13, 24), interval=120, show_grid=True,
            colormap=ListedColormap(["black", "blue", "red", "yellow"]))
```

<img src="../../resources/wireworld_xor.gif" width="50%"/>

The full source code for this example can be found [here](wireworld_xor_demo.py).

For more information, please refer to the following resources:

https://en.wikipedia.org/wiki/Wireworld

> Dewdney, A K (January 1990). "Computer recreations: The cellular automata programs that create Wireworld, Rugworld and other diversions". Scientific American. 262 (1): 146–149.