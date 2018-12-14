### Asynchronous Automata

Network Automata are usually processed synchronously. That is, each cell's
state is based strictly on the activity of its neighbourhood in the previous
timestep. For this reason, it doesn't matter in what order the cells are
updated. However, it is sometimes beneficial to update the states of the
cells asynchronously. There are various ways to implement such behaviour,
but normally one specifies an update order for the cells, or one allows the
cells to be updated in a random order, such that a cell's state is based
on the activity of its neighbourhood immediately. In practice, this means
that, in each "timestep", only a single cell is updated. The "true" timestep
is complete once all cells have been updated in an update cycle.

There are other ways to implement asynchronous dynamics in discrete
systems, but Netomaton supports the sequential kind of asynchronous updates,
described above, in the `AsynchronousRule` class.

The following example implements the elementary rule 60 sequential
automaton from Wolfram's NKS Notes on Chapter 9, section 10:
"Sequential cellular automata" (http://www.wolframscience.com/nks/notes-9-10--sequential-cellular-automata/):

```python
from netomaton import *

adjacencies = AdjacencyMatrix.cellular_automaton(n=21)

initial_conditions =[0]*10 + [1] + [0]*10

r = AsynchronousRule(activity_rule=lambda n, c, t: ActivityRule.nks_ca_rule(n, c, 60), update_order=range(1, 20))

activities, connectivities = evolve(initial_conditions, adjacencies, timesteps=19*20,
                                    activity_rule=r.activity_rule)

# plot every 19th row, including the first, as a cycle is completed every 19 rows
plot_grid(activities[::19])
```
<img src="https://raw.githubusercontent.com/lantunes/netomaton/master/resources/rule60async.png" width="40%"/>

The full source code for this example can be found [here](https://github.com/lantunes/netomaton/blob/master/demos/asynchronous_automata/asynchronous_automata_demo.py).
