import netomaton as ntm
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    a = 10
    b = 8/3
    r = 28
    dt = 0.005

    network = ntm.Network()
    network.add_edge("x", "x", weight=a)
    network.add_edge("y", "x", weight=a)
    network.add_edge("x", "y", weight=r)
    network.add_edge("z", "y", weight=1)
    network.add_edge("y", "y", weight=1)
    network.add_edge("x", "z", weight=1)
    network.add_edge("y", "z", weight=1)
    network.add_edge("z", "z", weight=b)

    initial_conditions = {"x": 1., "y": 1., "z": 1.}


    def activity_rule(ctx):
        node = ctx.node_label

        if node == "x":
            x, w_x = ctx.current_activity, ctx.connection_states["x"][0]["weight"]
            y, w_y = ctx.activities["y"], ctx.connection_states["y"][0]["weight"]
            activity = x + (w_y*y - w_x*x) * dt
        elif node == "y":
            y, w_y = ctx.current_activity, ctx.connection_states["y"][0]["weight"]
            x, w_x = ctx.activities["x"], ctx.connection_states["x"][0]["weight"]
            z, w_z = ctx.activities["z"], ctx.connection_states["z"][0]["weight"]
            activity = y + (w_x*x - w_y*y - x*w_z*z) * dt
        else:  # node == "z"
            z, w_z = ctx.current_activity, ctx.connection_states["z"][0]["weight"]
            x, w_x = ctx.activities["x"], ctx.connection_states["x"][0]["weight"]
            y, w_y = ctx.activities["y"], ctx.connection_states["y"][0]["weight"]
            activity = z + (w_x*x * w_y*y - w_z*z) * dt

        return activity

    trajectory = ntm.evolve(network, initial_conditions=initial_conditions,
                            activity_rule=activity_rule, timesteps=4500)

    points = np.array(ntm.get_activities_over_time_as_list(trajectory))
    X, Y, Z = points[:, 0], points[:, 1], points[:, 2]

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.scatter(X, Y, Z, s=.5)

    plt.show()
