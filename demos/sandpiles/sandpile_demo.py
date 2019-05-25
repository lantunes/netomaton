import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    sandpile = ntm.Sandpile(rows=60, cols=60)

    initial_conditions = np.random.randint(5, size=3600)

    def perturb(c, a, t):
        # drop a grain on some cell at the 85th timestep
        if t == 85 and c == 1034:
            return a + 1
        return a

    activities, _ = ntm.evolve(initial_conditions, sandpile.adjacencies, timesteps=110,
                               activity_rule=sandpile.activity_rule, perturbation=perturb)

    ntm.animate(activities, shape=(60, 60), interval=150)
