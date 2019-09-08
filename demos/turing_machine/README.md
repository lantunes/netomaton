### Turing Machine

There are two different ways that a Turing Machine can be described in
the context of the Netomaton framework:

1. as a Network Automaton with a single cell that carries
the state of the head, and a separate tape that is read from and written
to during processing;

2. as a Network Automaton with a number of cells representing the tape
(with the same local connectivity as an Elementary Cellular Automaton),
whose states are mutated as the tape is written to, and separate
variables for the state and current location of the head.

With approach **1**, an input _function_ must be specified which
provides the value from the tape that the head is currently reading. If
a desired state is reached (or a maximum number of steps have been
taken), the input function can return `None` to signal that the
evolution is complete, and the machine is halting. At each step, the
activity rule takes the input value, which is the value from the tape
that the head is currently reading, and determines the next state for
the cell, the new tape value at the current head position, and the
position of the head for the next timestep (the head can move left,
right, or not move at all).

With approach **2**, a pre-determined number of steps must be specified.
At each timestep, each cell is processed: if the cell's index does not
match the index of the head, then the cell's current activity is simply
returned; if the cell's index matches the index of the head, then the
Turing Machine's rule table is consulted, the new head state and
position are determined, and the new cell state is returned.