# Functional Network Automata

An example of a network automaton that contains both an activity rule and a topology rule. The topology rule simply 
removes the edge between two nodes if they are both activated (i.e. have an activity of "1" as opposed to "0"). The 
purpose of this demo is to illustrate the creation of topology rules that depend on changing node activities.

<img src="../../resources/fna.gif" width="50%"/>

The full source code for this example can be found [here](functional_network_automata_demo.py).
