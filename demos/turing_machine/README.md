### Turing Machine

There are two different ways that a Turing Machine can be described in
the context of the Netomaton framework:

1. as a Network Automaton with a single cell that carries
the state and position of the head, and a separate tape that is read
from and written to during processing;

2. as a Network Automaton with a number of cells representing the tape
(with the same local connectivity as an Elementary Cellular Automaton),
whose states change as the tape is written to, and separate variables
for the state and position of the head.

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

In the example below, a Turing machine is given with two possible states
for the head, and two possible states for each cell in the tape. It is a
reproduction of the Turing machine given on page 79 (figure (b)) of
Wolfram's [A New Kind of Science](https://www.wolframscience.com/nks/p79--turing-machines/).

```python
import netomaton as ntm
from netomaton import TuringMachine, TapeCentricTuringMachine

HEAD = {"up": 1, "down": 2}
CELL = {"on": 1, "off": 0}

rule_table = {
    HEAD['up']: {
        CELL['on']: [HEAD['up'], CELL['off'], TuringMachine.RIGHT],
        CELL['off']: [HEAD['down'], CELL['on'], TuringMachine.RIGHT]
    },
    HEAD['down']: {
        CELL['on']: [HEAD['up'], CELL['on'], TuringMachine.LEFT],
        CELL['off']: [HEAD['down'], CELL['on'], TuringMachine.LEFT]
    }
}

tm = TapeCentricTuringMachine(num_cells=21, rule_table=rule_table,
                              initial_head_state=HEAD['up'],
                              initial_head_position=3)

initial_conditions = [0] * 21

activities, _ = ntm.evolve(initial_conditions, tm.adjacencies,
                           activity_rule=tm.activity_rule, timesteps=61)

ntm.plot_grid(activities, cell_annotations=tm.head_activities(activities),
              show_grid=True)
```

<img src="../../resources/turing_2.png" width="50%"/>

The `TapeCentricTuringMachine` is based on approach **2**, described
above. The complete source code for this example is [here](turing_machine_demo_2.py).

In the example above, the initial state (i.e. the tape) is very simple,
and there are only four rules. But with just a little more complexity,
it isn't long before a universal Turing machine is found. In the
following example, a Turing machine with 2 states for the head, and 5
states for each cell in the tape is demonstrated. This is the simple
universal Turing machine described in Wolfram's
[New Kind of Science](https://www.wolframscience.com/nks/p707--universality-in-turing-machines-and-other-systems/),
which emulates ECA Rule 110 (also known to be universal).

```python
import netomaton as ntm
from netomaton import TuringMachine, TapeCentricTuringMachine

HEAD = {"up": 1, "down": 2}
CELL = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}

rule_table = {
    HEAD['up']: {
        CELL['a']: [HEAD['up'], CELL['b'], TuringMachine.LEFT],
        CELL['b']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
        CELL['c']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
        CELL['d']: [HEAD['down'], CELL['e'], TuringMachine.RIGHT],
        CELL['e']: [HEAD['down'], CELL['d'], TuringMachine.LEFT]
    },
    HEAD['down']: {
        CELL['a']: [HEAD['up'], CELL['d'], TuringMachine.LEFT],
        CELL['b']: [HEAD['up'], CELL['a'], TuringMachine.RIGHT],
        CELL['c']: [HEAD['up'], CELL['e'], TuringMachine.RIGHT],
        CELL['d']: [HEAD['down'], CELL['e'], TuringMachine.RIGHT],
        CELL['e']: [HEAD['down'], CELL['c'], TuringMachine.LEFT]
    }
}

tape = "bbbbbbaeaaaaaaa"

tm = TapeCentricTuringMachine(num_cells=len(tape), rule_table=rule_table,
                              initial_head_state=HEAD['up'],
                              initial_head_position=8)

initial_conditions = [CELL[t] for t in tape]

activities, _ = ntm.evolve(initial_conditions, tm.adjacencies,
                           activity_rule=tm.activity_rule, timesteps=58)

ntm.plot_grid(activities, cell_annotations=tm.head_activities(activities),
              show_grid=True)
```

<img src="../../resources/turing_2c.png" width="50%"/>

The plot on the right is the compressed output of running the machine
for 5000 steps, and it clearly demonstrates that Rule 110 is emulated.
(The code for this plot can be seen [here](turing_machine_demo_2c.py),
along with the full source code for this example.)

The `HeadCentricTuringMachine` is based on approach **1**, described
above. It is used in the example below, to demonstrate a Turing
machine with 7 states for the head, and 7 states for each cell in the
tape, for the language _L = {a<sup>n</sup>b<sup>n</sup>c<sup>n</sup> | n > 0}_.
If the evolution of the automaton settles on the head state 'q6', then
the string is accepted.

```python
import netomaton as ntm
from netomaton import TuringMachine, HeadCentricTuringMachine

HEAD = {"q0": 0, "q1": 1, "q2": 2, "q3": 3, "q4": 4, "q5": 5, "q6": 6}
CELL = {" ": 0, "a": 1, "b": 2, "c": 3, "x": 4, "y": 5, "z": 6}

rule_table = {
    HEAD['q0']: {
        CELL['a']: [HEAD['q1'], CELL['x'], TuringMachine.RIGHT],
        CELL[' ']: [HEAD['q6'], CELL[' '], TuringMachine.STAY],
        ...
    }
}

tape = "  aabbcc  "

tm = HeadCentricTuringMachine(tape=[CELL[t] for t in tape], rule_table=rule_table,
                              initial_head_state=HEAD['q0'], initial_head_position=2,
                              terminating_state=HEAD['q6'], max_timesteps=50)

activities, _ = ntm.evolve(tm.initial_conditions, tm.adjacencies,
                           activity_rule=tm.activity_rule,
                           input=tm.input_function)

tape_history, head_activities = tm.activities_for_plotting(activities)

ntm.plot_grid(tape_history, cell_annotations=head_activities,
              show_grid=True)
```

<img src="../../resources/turing_1b.png" width="50%"/>

Note that the `evolve` function is given the `input` parameter, which in
this case is a function, which returns the value the head is currently
reading, and `None` when (and if) the machine reaches the terminating
state of 'q6'. The full source code for this example is [here](turing_machine_demo_1b).

Both the `TapeCentricTuringMachine` and `HeadCentricTuringMachine` will
produce the same results. However, the `HeadCentricTuringMachine` may
conceptually be more appropriate when thinking about how a Turing
machine can be described as Network Automaton. The tape is, after all, a
passive element that serves both as input and memory, while the head is
where the system's definitive state is stored. If one were to imagine
adding more cells to this Network Automaton, with approach **1**, one is
simply adding more cells to the tape, but with approach **2**, one is
adding more heads, each with their own tape, which seems to be a much
more meaningful change.
