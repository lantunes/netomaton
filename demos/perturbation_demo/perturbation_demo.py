import netomaton as ntm
import numpy as np


if __name__ == '__main__':
    network = ntm.topology.cellular_automaton(n=200)
    initial_conditions = [0] * 100 + [1] + [0] * 99

    noise_amount = 0.02

    def perturbation(pctx):
        # from page 976 of Stephen Wolfram's "A New Kind of Science", the perturbation amount is:
        # v + Sign[v - 1/2]Random[]δ
        return pctx.node_activity + np.sign(pctx.node_activity - 1/2)*np.random.uniform()*noise_amount

    def algebraic_rule_90(ctx):
        """
        This rule implements the continuous cellular automaton with generalization of Rule 90, described on
        pages 325 and 976 of Stephen Wolfram's "A New Kind of Science".
        """
        x = ctx.neighbourhood_activities[0] + ctx.neighbourhood_activities[2]
        # λ[x_] := Exp[-10 (x - 1)^2] + Exp[-10 (x - 3)^2]
        result = np.exp(-10*((x-1)**2)) + np.exp(-10*((x-3)**2))

        return result

    def algebraic_rule_30(ctx):
        """
        This rule implements the continuous cellular automaton with generalization of Rule 30, described on
        pages 325 and 976 of Stephen Wolfram's "A New Kind of Science".
        """
        a, b, c = ctx.neighbourhood_activities
        x = a + b + c + (b * c)
        # λ[x_] := Exp[-10 (x - 1)^2] + Exp[-10 (x - 3)^2]
        result = np.exp(-10*((x-1)**2)) + np.exp(-10*((x-3)**2))

        return result

    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, timesteps=100,
                            activity_rule=algebraic_rule_30, perturbation=perturbation)

    ntm.plot_activities(trajectory)
