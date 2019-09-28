### Langton's Lambda and Measures of Complexity

One way to specify Cellular Automata rules is with rule tables. Rule tables are enumerations of all possible
neighbourhood states together with their node state mappings. For any given neighbourhood state, a rule table provides
the associated node state value. Netomaton provides a built-in function for creating random rule tables. The following
snippet demonstrates its usage:
```python
import netomaton as ntm

rule_table, actual_lambda, quiescent_state = ntm.random_rule_table(lambda_val=0.45, k=4, r=2,
                                                                   strong_quiescence=True, isotropic=True)

adjacency_matrix = ntm.network.cellular_automaton(n=128, r=2)

initial_conditions = ntm.init_random(128, k=4)

# use the built-in table_rule to use the generated rule table
activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=200,
                           activity_rule=lambda ctx: ntm.table_rule(ctx, rule_table))
```
The following plots demonstrate the effect of varying the lambda parameter:

<img src="../../resources/phase_transition.png" width="100%"/>

The source code for the example above can be found [here](rule_table_demo.py).

C. G. Langton describes the lambda parameter, and the transition from order to criticality to chaos in Cellular
Automata while varying the lambda parameter, in the paper:

> Langton, C. G. (1990). Computation at the edge of chaos: phase transitions and emergent computation. Physica D: Nonlinear Phenomena, 42(1-3), 12-37.

#### Measures of Complexity

Netomaton provides various built-in functions which can act as measures of complexity in the automata being
examined.

##### Average Node Entropy

Average node entropy can reveal something about the presence of information within automata dynamics. The
built-in function `average_node_entropy` provides the average Shannon entropy per single node in a given
automaton. The following snippet demonstrates the calculation of the average node entropy:

```python
import netomaton as ntm

adjacency_matrix = ntm.network.cellular_automaton(n=200)

initial_conditions = ntm.init_random(200)

activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=1000,
                           activity_rule=lambda ctx: ntm.rules.nks_ca_rule(ctx, 30))

# calculate the average node entropy; the value will be ~0.999 in this case
avg_node_entropy = ntm.average_node_entropy(activities)
```

The source code for the example above can be found [here](average_node_entropy_demo.py).

The following plots illustrate how average node entropy changes as a function of lambda:

<img src="../../resources/avg_node_entropy.png" width="100%"/>

##### Average Mutual Information

The degree to which a node state is correlated to its state in the next time step can be described using mutual
information. Ideal levels of correlation are required for effective processing of information. The built-in function
`average_mutual_information` provides the average mutual information between a node and itself in the next time step
(the temporal distance can be adjusted). The following snippet demonstrates the calculation of the average mutual
information:

```python
import netomaton as ntm

adjacency_matrix = ntm.network.cellular_automaton(n=200)

initial_conditions = ntm.init_random(200)

activities, _ = ntm.evolve(initial_conditions, adjacency_matrix, timesteps=1000,
                           activity_rule=lambda ctx: ntm.rules.nks_ca_rule(ctx, 30))

# calculate the average mutual information between a node and itself in the next time step
avg_mutual_information = ntm.average_mutual_information(activities)
```

The source code for the example above can be found [here](average_mutual_information_demo.py).

The following plots illustrate how average mutual information changes as a function of lambda:

<img src="../../resources/avg_mutual_information.png" width="100%"/>

The groups of plots above were created using the source code found [here](rule_table_walkthrough_demo.py).
