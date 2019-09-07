import netomaton as ntm

if __name__ == "__main__":

    # A Turing machine with two possible states for the head, and two possible states for each cell in the tape.
    # A reproduction of the Turing machine given on page 79 (figure (b)) of NKS
    #   (https://www.wolframscience.com/nks/p79--turing-machines/)

    HEAD = {"up": 1, "down": 2}
    CELL = {"on": 1, "off": 0}
    POS = {"left": 0, "right": 2}

    rule_table = {
        HEAD['up']: {
            CELL['on']:  [HEAD['up'], CELL['off'], POS['right']],
            CELL['off']: [HEAD['down'], CELL['on'], POS['right']]
        },
        HEAD['down']: {
            CELL['on']:  [HEAD['up'], CELL['on'], POS['left']],
            CELL['off']: [HEAD['down'], CELL['on'], POS['left']]
        }
    }

    # the head starts in the 'up' state at position 3 on the tape
    head_list = [(HEAD['up'], 3)]
    curr_t = 1

    def turing_machine(n, c, t):
        global curr_t
        if t != curr_t:
            curr_t = t
        head_state, head_pos = head_list[curr_t - 1]
        cell_state = n.current_activity
        if c == head_pos:
            next_head_state, new_cell_state, pos = rule_table[head_state][cell_state]
            head_list.append((next_head_state, n.neighbour_indices[pos]))
            return new_cell_state
        return cell_state

    adjacencies = ntm.network.cellular_automaton(21)

    initial_conditions = [0]*21

    activities, _ = ntm.evolve(initial_conditions, adjacencies, activity_rule=turing_machine, timesteps=61)

    # create the annotations for the head state
    cell_annotations = [[None for i in range(21)] for j in range(61)]
    for i, h in enumerate(head_list):
        cell_annotations[i][h[1]] = str(h[0])

    ntm.plot_grid(activities, cell_annotations=cell_annotations, show_grid=True)
