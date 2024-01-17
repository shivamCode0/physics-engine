from typing_extensions import deprecated
import pygame
from config import *
import math
import numpy as np
import scipy as sp
import scipy.spatial as sps


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

    @deprecated
    @property
    def x(self):
        return self.pos[0]

    @deprecated
    @x.setter
    def x(self, value):
        self.pos[0] = value

    @deprecated
    @property
    def y(self):
        return self.pos[1]

    @deprecated
    @y.setter
    def y(self, value):
        self.pos[1] = value

    @deprecated
    @property
    def vx(self):
        return self.v[0]

    @deprecated
    @vx.setter
    def vx(self, value):
        self.v[0] = value

    @deprecated
    @property
    def vy(self):
        return self.v[1]

    @deprecated
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
        self.v += np.array(force) / self.mass * timedelta


def elastic_collision(m_1, m_2, v_1i, v_2i):
    v_1f = (m_1 * v_1i + m_2 * v_2i - m_2 * (2 * m_1 * v_1i - m_1 * v_2i + m_2 * v_2i) / (m_1 + m_2)) / m_1
    v_2f = (2 * m_1 * v_1i - m_1 * v_2i + m_2 * v_2i) / (m_1 + m_2)
    return v_1f, v_2f


def inelastic_collision(m_1, m_2, v_1i, v_2i):
    v_1f = (m_1 * v_1i + m_2 * v_2i) / (m_1 + m_2)
    v_2f = (m_1 * v_1i + m_2 * v_2i) / (m_1 + m_2)
    return v_1f, v_2f


def partially_elastic_collision(elasticity, m_1, m_2, v_1i, v_2i):
    # Calculate the relative velocity before collision
    relative_velocity_before = v_1i - v_2i

    # Calculate the relative velocity after collision based on elasticity
    relative_velocity_after = elasticity * relative_velocity_before

    # Calculate final velocities
    v_1f = v_1i - (m_2 * relative_velocity_after) / (m_1 + m_2)
    v_2f = v_2i + (m_1 * relative_velocity_after) / (m_1 + m_2)

    return v_1f, v_2f


def percent_inelastic_collision(
    percent,
    m_1,
    m_2,
    v_1i,
    v_2i,
):
    # weighted average between elastic and inelastic collisions
    v1_elastic, v2_elastic = elastic_collision(m_1, m_2, v_1i, v_2i)
    v1_inelastic, v2_inelastic = inelastic_collision(m_1, m_2, v_1i, v_2i)
    v_1f = percent * v1_elastic + (1 - percent) * v1_inelastic
    v_2f = percent * v2_elastic + (1 - percent) * v2_inelastic
    return v_1f, v_2f


def update_physics(circle: Circle, timedelta: float, circles: list[Circle]):
    # print frame rate
    # print(1 / timedelta)
    # Update velocity based on arrow key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle.apply_force((-force_amt, 0), timedelta)
    if keys[pygame.K_RIGHT]:
        circle.apply_force((force_amt, 0), timedelta)
    if keys[pygame.K_UP]:
        circle.apply_force((0, -force_amt), timedelta)
    if keys[pygame.K_DOWN]:
        circle.apply_force((0, force_amt), timedelta)

    # Update velocity based on gravity
    # F_g = G * m1 * m2 / r^2
    for other_circle in circles:
        if other_circle is not circle:
            # Update velocity based on gravity
            combined_radius = circle.radius + other_circle.radius
            distance = sps.distance.euclidean(circle.pos, other_circle.pos)
            r = max(distance, combined_radius)  # prevent division by zero
            F_g = G * circle.mass * other_circle.mass / r**2
            theta = np.arctan2(other_circle.y - circle.y, other_circle.x - circle.x)
            circle.apply_force((-F_g * np.cos(theta), -F_g * np.sin(theta)), timedelta)

            # Update velocity based on collisions
            if (circle.id < other_circle.id) and (
                # combined_radius - distance < 1
                True
            ):  # only check each pair of circles once
                if distance < combined_radius:
                    # Collision has occurred
                    # use both conservation of momentum and conservation of kinetic energy
                    elasticity = 0.5  # change this to change elasticity
                    v1x, v2x = elastic_collision(elasticity, circle.mass, other_circle.mass, circle.vx, other_circle.vx)
                    v1y, v2y = elastic_collision(elasticity, circle.mass, other_circle.mass, circle.vy, other_circle.vy)

                    circle.vx = v1x

                    circle.vy = v1y
                    other_circle.vx = v2x
                    other_circle.vy = v2y

    # if outside bounds, bounce
    if circle.x < circle.radius:
        circle.vx = abs(circle.vx)
    elif circle.x > width - circle.radius:
        circle.vx = -abs(circle.vx)
    if circle.y < circle.radius:
        circle.vy = abs(circle.vy)
    elif circle.y > height - circle.radius:
        circle.vy = -abs(circle.vy)
    # Update position based on velocity and elapsed time
    circle.x += circle.vx * timedelta
    circle.y += circle.vy * timedelta
