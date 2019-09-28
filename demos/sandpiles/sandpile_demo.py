import netomaton as ntm
import numpy as np


if __name__ == '__main__':

    sandpile = ntm.Sandpile(rows=60, cols=60)

    initial_conditions = np.random.randint(5, size=3600)

    def perturb(pctx):
        # drop a grain on some cell at the 85th timestep
        if pctx.timestep == 85 and pctx.cell_index == 1034:
            return pctx.cell_activity + 1
        return pctx.cell_activity

    activities, _ = ntm.evolve(initial_conditions, sandpile.adjacencies, timesteps=110,
                               activity_rule=sandpile.activity_rule, perturbation=perturb)

    ntm.animate(activities, shape=(60, 60), interval=150)
