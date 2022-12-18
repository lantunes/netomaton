# Sandpiles

Netomaton offers an implementation of the Abelian sandpile model.

```python
import netomaton as ntm
import numpy as np

sandpile = ntm.Sandpile(rows=60, cols=60)

initial_conditions = np.random.randint(5, size=3600)

def perturb(pctx):
    # drop a grain on some node at the 85th timestep
    if pctx.timestep == 85 and pctx.node_label == 1034:
        return pctx.node_activity + 1
    return pctx.node_activity

trajectory = ntm.evolve(initial_conditions=initial_conditions, network=sandpile.network,
                        activity_rule=sandpile.activity_rule, perturbation=perturb, timesteps=110)

ntm.animate_activities(trajectory, shape=(60, 60), interval=150)
```

<img src="../../resources/sandpile.gif" width="50%"/>

The full source code for this example can be found [here](sandpile_demo.py).

See the following for more information on Abelian sandpile models:

> Bak, Per, Chao Tang, and Kurt Wiesenfeld. "Self-organized criticality." Physical review A 38.1 (1988): 364.