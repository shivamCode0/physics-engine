import pygame
from config import *
import math
import numpy as np
import scipy as sp
import scipy.spatial as sps
from Circle import Circle


def elastic_collision(m_1, m_2, v_1i, v_2i):
    v_1f = (m_1 * v_1i + m_2 * v_2i - m_2 * (2 * m_1 * v_1i - m_1 * v_2i + m_2 * v_2i) / (m_1 + m_2)) / m_1
    v_2f = (2 * m_1 * v_1i - m_1 * v_2i + m_2 * v_2i) / (m_1 + m_2)
    return v_1f, v_2f


def inelastic_collision(m_1, m_2, v_1i, v_2i):
    v_1f = (m_1 * v_1i + m_2 * v_2i) / (m_1 + m_2)
    v_2f = (m_1 * v_1i + m_2 * v_2i) / (m_1 + m_2)
    return v_1f, v_2f


# v_\text{a} = \frac{m_\text{a} u_\text{a} + m_\text{b} u_\text{b} + m_\text{b} C_R(u_\text{b}-u_\text{a})}{m_\text{a}+m_\text{b}}
# v_\text{b} = \frac{m_\text{a} u_\text{a} + m_\text{b} u_\text{b} + m_\text{a} C_R(u_\text{a}-u_\text{b})}{m_\text{a}+m_\text{b}}
"""
𝑣
a
 is the final velocity of the first object after impact

𝑣
b
 is the final velocity of the second object after impact
𝑢
a
 is the initial velocity of the first object before impact
𝑢
b
 is the initial velocity of the second object before impact
𝑚
a
 is the mass of the first object
𝑚
b
 is the mass of the second object
"""


def partially_elastic_collision(cr, m1, m2, v1i, v2i):
    m = m1 + m2
    p_i = m1 * v1i + m2 * v2i
    v_diff = v1i - v2i
    v_a = (p_i - m2 * cr * v_diff) / m
    v_b = (p_i + m1 * cr * v_diff) / m
    return v_a, v_b


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
            F_g1 = G * circle.mass * other_circle.mass / r**2
            theta = np.arctan2(other_circle.y - circle.y, other_circle.x - circle.x)
            F_g = np.array([F_g1 * np.cos(theta), F_g1 * np.sin(theta)])
            if distance < combined_radius:
                F_g *= -10
            circle.apply_force(F_g, timedelta)

            # Update velocity based on collisions
            if circle.id < other_circle.id:  # only check each pair of circles once
                if distance < combined_radius:
                    # Collision has occurred

                    # if moving away, skip
                    timedelta2 = timedelta / 1000
                    # movingaway = sps.distance.euclidean(
                    #     circle.v * timedelta2 + circle.pos, other_circle.v * timedelta2 + other_circle.pos
                    # ) > sps.distance.euclidean(circle.pos, other_circle.pos)
                    # if not movingaway:
                    circle.v, other_circle.v = partially_elastic_collision(
                        C_R, circle.mass, other_circle.mass, circle.v, other_circle.v
                    )

            # Repulsion force
            # F_r = k * (r - r_0)
            if distance < combined_radius:
                k = 1
                r_0 = combined_radius
                F_r1 = k * (r - r_0)
                theta = np.arctan2(other_circle.y - circle.y, other_circle.x - circle.x)
                F_r = np.array([F_r1 * np.cos(theta), F_r1 * np.sin(theta)])
                circle.apply_force(F_r, timedelta)

    # if outside bounds, bounce
    if circle.x < circle.radius:
        circle.vx = abs(circle.vx) * WALL_C_R
    elif circle.x > width - circle.radius:
        circle.vx = -abs(circle.vx) * WALL_C_R
    if circle.y < circle.radius:
        circle.vy = abs(circle.vy) * WALL_C_R
    elif circle.y > height - circle.radius:
        circle.vy = -abs(circle.vy) * WALL_C_R
    # Update position based on velocity and elapsed time
    circle.x += circle.vx * timedelta
    circle.y += circle.vy * timedelta
