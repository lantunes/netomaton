### Animating Network Automata

Network Automata can be animated with the Netomaton `animate` function.

For example, the evolution of a 2D 60x60 cellular automaton can be
visualized using:
```python
ntm.animate(activities, shape=(60, 60), interval=150)
```
<img src="../../resources/animation2D.gif" width="40%"/>

The evolution of a 1D celluar automaton with 200 cells can be visualized
using:
```python
# note that the shape specified is a tuple containing only a single value
ntm.animate(activities, shape=(200,))
```
<img src="../../resources/animation1D.gif" width="40%"/>

Because a Network Automaton consists of a vector of activities at each
timestep, that vector can be reshaped and visualized however desired.
For example, the evolution of a 1D cellular automaton with 225 cells
can be visualized as if it were a 2D cellular automation, using:
```python
ntm.animate(activities, shape=(15, 15))
```
<img src="../../resources/animation1Db.gif" width="40%"/>

The full source code for these examples can be found [here](animation_demo.py).
