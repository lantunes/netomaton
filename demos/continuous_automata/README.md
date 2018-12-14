### Continuous Automata

Network Automata needn't consist of discrete activities. The units in an
automaton can also take on continuous-valued activities.

The example below implements a continuous-valued cellular automaton
from Wolfram's NKS book, found on page 157:

```python
import math
from netomaton import *

adjacencies = AdjacencyMatrix.cellular_automaton(n=200)

initial_conditions = [0.0]*100 + [1.0] + [0.0]*99

# NKS page 157
def activity_rule(n, c, t):
    activities = n.activities
    result = (sum(activities) / len(activities)) * (3 / 2)
    frac, whole = math.modf(result)
    return frac

activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=150,
                                    activity_rule=activity_rule)

plot_grid(activities)
```
<img src="https://raw.githubusercontent.com/lantunes/netomaton/master/resources/continuous_ca.png" width="40%"/>