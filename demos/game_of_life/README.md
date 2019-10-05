# Conway's Game of Life

Conway's Game of Life is a well-known 2D Cellular Automaton.

<img src="../../resources/game_of_life.gif" width="65%"/>

It can be defined with the Netomaton framework:

```python
import netomaton as ntm

adjacency_matrix = ntm.network.cellular_automaton2d(rows=60, cols=60, r=1, neighbourhood='Moore')

initial_conditions = ntm.init_simple2d(60, 60)

# Light Weight Space Ship (LWSS)
initial_conditions[1125] = 1
initial_conditions[1128] = 1
initial_conditions[1184] = 1
initial_conditions[1244] = 1
initial_conditions[1248] = 1
initial_conditions[1304] = 1
initial_conditions[1305] = 1
initial_conditions[1306] = 1
initial_conditions[1307] = 1

# Glider
initial_conditions[1710] = 1
initial_conditions[1771] = 1
initial_conditions[1829] = 1
initial_conditions[1830] = 1
initial_conditions[1831] = 1

# Blinker
initial_conditions[2415] = 1
initial_conditions[2416] = 1
initial_conditions[2417] = 1

activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=60,
                           activity_rule=lambda ctx: ntm.rules.game_of_life_rule(ctx))

ntm.animate(activities, shape=(60, 60))
```

The full source code for this example can be found [here](game_of_life_demo.py).

For more information about Conway's Game of Life, see:

> Conway, J. (1970). The game of life. Scientific American, 223(4), 4.
