### 1D Cellular Automata with Totalistic Rules

The number of states, or colors, that a cell in a Cellular Automaton can adopt is given by _k_. For example, in a binary Cellular Automaton a cell can
assume only values of 0 and 1, and thus has _k_ = 2. A built-in function, `totalistic_ca`,
is an implementation of the [Totalistic Cellular Automaton rule](http://mathworld.wolfram.com/TotalisticCellularAutomaton.html),
as described in [Wolfram's NKS](https://www.wolframscience.com/nks/). The code snippet below illustrates using this rule.
A value of _k_ of 3 is used, but any value between (and including) 2 and 36 is currently supported. The rule number is
given in base 10 but is interpreted as the rule in base _k_ (thus rule 777 corresponds to '1001210' when _k_ = 3).

```python
import netomaton as ntm

adjacency_matrix = ntm.network.cellular_automaton(n=200)

initial_conditions = [0]*100 + [1] + [0]*99

activities, adjacencies = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=100,
                                     activity_rule=lambda ctx: ntm.rules.totalistic_ca(ctx, k=3, rule=777))

ntm.plot_grid(activities)
```

<img src="../../resources/tot3_rule777.png" width="50%"/>

The full source code for this example can be found [here](totalistic_ca_demo.py).
