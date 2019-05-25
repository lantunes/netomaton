### Perturbations

Network Automata may be perturbed at any point in time during their
evolution. This may model the effects of some external forcing applied
to the system as it evolves. Many natural systems are continuously
perturbed, and not allowed to reach an equilibrium, or steady state.
Indeed, perturbations are important elements in the study of
non-equilibrium systems.

Netomaton supports perturbations. A perturbation is
simply a function that accepts the cell index, its computed activity,
and the timestep, and returns the new activity for that cell.


Consider the cellular automaton Rule 30 below, which is perturbed at
every timestep such that cell with index 100 is changed randomly to
either a 0 or a 1:
```python
adjacencies = ntm.AdjacencyMatrix.cellular_automaton(n=200)
initial_conditions = [0] * 100 + [1] + [0] * 99

def perturb(c, a, t):
    """
    Mutates the value of the cell with index 100 at each timestep, making it either 0 or 1 randomly.
    """
    if c == 100:
        return np.random.randint(2)
    return a

activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                           activity_rule=lambda n, c, t: ntm.ActivityRule.nks_ca_rule(n, c, 30),
                           perturbation=perturb)

ntm.plot_grid(activities)
```
<img src="../../resources/perturbation.png" width="50%"/>

The full source code for this example can be found [here](perturbation_eca_demo.py).
