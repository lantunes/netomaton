import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Turtle:
    def __init__(self, start_x=0, start_y=0, start_orientation=0):
        """
        A simple Turtle graphics implementation using Matplotlib for graphics.

        :param start_x: the starting x-coordinate (optional, default is 0)

        :param start_y: the starting y-coordinate (optional, default is 0)

        :param start_orientation: the starting orientation in degrees (optional, default is 0)
        """
        self.x = start_x
        self.y = start_y
        self.orientation = start_orientation
        self.trajectory = []
        self._stack = []

    def forward(self, distance=1):
        """
        Move the Turtle forward, from the current orientation, by the given amount.

        :param distance: the amount by which to move the Turtle (default is 1)
        """
        angle = math.radians(self.orientation)
        new_x = math.sin(angle) * distance + self.x
        new_y = math.cos(angle) * distance + self.y
        p1 = [self.x, self.y]
        p2 = [new_x, new_y]
        x_values = [p1[0], p2[0]]
        y_values = [p1[1], p2[1]]
        self.trajectory.append((x_values, y_values))
        self.x = new_x
        self.y = new_y

    def rotate(self, degrees):
        """
        Rotate the Turtle by the given number of degrees. A positive number turns right, and a negative number
        turns left.

        :param degrees: the amount by which to turn, in degrees
        """
        self.orientation += degrees

    def push(self):
        """
        Pushes the current state (x- and y-coordinates, and orientation) onto an internal stack.
        """
        self._stack.append((self.x, self.y, self.orientation))

    def pop(self):
        """
        Pops the last stored state (x- and y-coordinates, and orientation) from the internal stack, and sets
        the state of the Turtle to that state.
        """
        x, y, orientation = self._stack.pop()
        self.x = x
        self.y = y
        self.orientation = orientation

    @property
    def pos(self):
        """
        Return the current position of the Turtle.

        :return: a 2-tuple, representing the x and y coordinates of the Turtle
        """
        return self.x, self.y

    @property
    def abs(self):
        """
        The magnitude of the vector describing the current position of the Turtle (i.e. the distance from the origin).

        :return: the absolute value of the position vector
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def plot(self, marker=""):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        for state in self.trajectory:
            plt.plot(state[0], state[1], marker=marker, color="black")

        plt.gca().axes.xaxis.set_ticklabels([])
        plt.gca().axes.yaxis.set_ticklabels([])
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def animate(self, save=False, interval=50, dpi=80, marker="", repeat=False, fps=50):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        x_vals = [s[0] for s in self.trajectory]
        max_x = np.max(x_vals)
        min_x = np.min(x_vals)
        max_x += 0.05*(max_x - min_x)
        min_x -= 0.05*(max_x - min_x)
        y_vals = [s[1] for s in self.trajectory]
        max_y = np.max(y_vals)
        min_y = np.min(y_vals)
        max_y += 0.05*(max_y - min_y)
        min_y -= 0.05*(max_y - min_y)

        def update(t):
            plt.plot(self.trajectory[t][0], self.trajectory[t][1], marker=marker, color="black")
            if t == len(self.trajectory) - 1 and repeat:
                ax.clear()
                ax.xaxis.set_ticklabels([])
                ax.yaxis.set_ticklabels([])
                ax.set_xticks([])
                ax.set_yticks([])
                plt.xlim(min_x, max_x)
                plt.ylim(min_y, max_y)

        ani = animation.FuncAnimation(fig, update, frames=len(self.trajectory), interval=interval,
                                      save_count=len(self.trajectory), repeat=repeat)

        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)

        plt.gca().axes.xaxis.set_ticklabels([])
        plt.gca().axes.yaxis.set_ticklabels([])
        plt.xticks([])
        plt.yticks([])

        if save:
            ani.save('turtle.gif', dpi=dpi, writer="imagemagick", fps=fps)
        plt.show()
