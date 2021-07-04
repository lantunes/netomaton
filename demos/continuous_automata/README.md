# Continuous Automata

Network Automata needn't consist of discrete activities. The units in an
automaton can also take on continuous-valued activities (i.e. states).

The example below implements a continuous-valued Cellular Automaton
from Wolfram's NKS book, found on page 157:

```python
import math
import netomaton as ntm

network = ntm.topology.cellular_automaton(n=200)

initial_conditions = [0.0]*100 + [1.0] + [0.0]*99

 # NKS page 157
def activity_rule(ctx):
    activities = ctx.neighbourhood_activities
    result = (sum(activities) / len(activities)) * (3 / 2)
    frac, whole = math.modf(result)
    return frac

trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network,
                        activity_rule=activity_rule, timesteps=150)

ntm.plot_activities(trajectory)
```

<img src="../../resources/continuous_ca.png" width="40%"/>

The full source code for this example can be found [here](continuous_automata_demo.py).
