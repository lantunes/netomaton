import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    adjacencies = ntm.network.cellular_automaton(n=200)
    initial_conditions = [0] * 100 + [1] + [0] * 99

    noise_amount = 1.05

    def perturbation(c, a, t):
        # from page 976 of Stephen Wolfram's "A New Kind of Science", the perturbation amount is:
        # v + Sign[v - 1/2]Random[]δ
        return a + np.sign(a - 1/2)*np.random.uniform()*noise_amount

    def noisy_rule_90(n, c, t):
        """
        This rule implements the continuous cellular automaton with generalization of Rule 90, described on
        pages 325 and 976 of Stephen Wolfram's "A New Kind of Science".
        """
        x = n.activities[0] + n.activities[2]
        # λ[x_] := Exp[-10 (x - 1)^2] + Exp[-10 (x - 3)^2]
        result = np.exp(-10*((x-1)**2)) + np.exp(-10*((x-3)**2))

        return result

    def noisy_rule_30(n, c, t):
        """
        This rule implements the continuous cellular automaton with generalization of Rule 30, described on
        pages 325 and 976 of Stephen Wolfram's "A New Kind of Science".
        """
        x = n.activities[0] + n.activities[1] + n.activities[2] + (n.activities[1]*n.activities[2])
        # λ[x_] := Exp[-10 (x - 1)^2] + Exp[-10 (x - 3)^2]
        result = np.exp(-10*((x-1)**2)) + np.exp(-10*((x-3)**2))

        return result

    activities, _ = ntm.evolve(initial_conditions, adjacencies, timesteps=100,
                               activity_rule=noisy_rule_30, perturbation=perturbation)

    ntm.plot_grid(activities)
