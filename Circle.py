import numpy as np


class Circle:
    id_counter = 0  # Class variable to keep track of id

    id: int  # New id variable

    mass: float
    radius: float
    # x: float
    # y: float
    # vx: float = 0.0
    # vy: float = 0.0
    pos = np.array([0.0, 0.0])
    v = np.array([0.0, 0.0])

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos[1] = value

    @property
    def vx(self):
        return self.v[0]

    @vx.setter
    def vx(self, value):
        self.v[0] = value

    @property
    def vy(self):
        return self.v[1]

    @vy.setter
    def vy(self, value):
        self.v[1] = value

    # def __init__(self, mass, radius, x, y, vx=0.0, vy=0.0):
    def __init__(self, mass, radius, pos, v=(0.0, 0.0)):
        self.mass = mass
        self.radius = radius
        # self.x = x
        # self.y = y
        # self.vx = vx
        # self.vy = vy
        self.pos = np.array(pos)
        self.v = np.array(v)
        self.id = Circle.id_counter  # Assign the current id_counter value to the id
        Circle.id_counter += 1  # Increment id_counter for the next instance

    def apply_force(self, force, timedelta):
        # fx, fy = force
        # self.vx += fx / self.mass * timedelta
        # self.vy += fy / self.mass * timedelta
        self.v = self.v + np.array(force) / self.mass * timedelta
