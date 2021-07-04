# Perturbations

Network Automata may be perturbed at any point in time during their
evolution. This may model the effects of some external forcing applied
to the system as it evolves. Many natural systems are continuously
perturbed, and not allowed to reach an equilibrium, or steady state.
Indeed, perturbations are important elements in the study of
non-equilibrium systems.

Netomaton supports perturbations. A perturbation is
simply a function that accepts a `PerturbationContext`, which contains
the node index, its computed activity, the timestep, and any input to
the node, and returns the new activity for that node.

Consider the Cellular Automaton Rule 30 below, which is perturbed at
every timestep such that node with index 100 is changed randomly to
either a 0 or a 1:
```python
network = ntm.topology.cellular_automaton(n=200)
initial_conditions = [0] * 100 + [1] + [0] * 99

def perturb(pctx):
    """
    Mutates the value of the node with index 100 at each timestep, making it either 0 or 1 randomly.
    """
    if pctx.node_label == 100:
        return np.random.randint(2)
    return pctx.node_activity

trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100,
                        activity_rule=ntm.rules.nks_ca_rule(30), perturbation=perturb)

ntm.plot_activities(trajectory)
```
<img src="../../resources/perturbation.png" width="50%"/>

Another way to perturb a Network Automaton is to simply wrap the activity
rule function with yet another function. Such an approach offers more
control over when the activity is determined, and what is done with it.
Below is an example of a perturbed Cellular Automaton rule 90R:
```python
network = ntm.topology.cellular_automaton(n=200)
initial_conditions = np.random.randint(0, 2, 200)

def perturbed_rule(ctx):
    rule = ntm.rules.nks_ca_rule(90)
    if ctx.timestep % 10 == 0:
        return 1
    return rule(ctx)

trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100,
                        activity_rule=ntm.ReversibleRule(perturbed_rule), past_conditions=[initial_conditions])

ntm.plot_activities(trajectory)
```
<img src="../../resources/perturbation_reversible.png" width="50%"/>

The full source code for these examples can be found
[here](perturbation_eca_demo.py) and [here](perturbation_reversible_demo.py).
