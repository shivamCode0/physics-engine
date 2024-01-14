from dataclasses import dataclass
import pygame
import sys
import numpy as np
import math
import scipy as sp
import scipy.spatial as sps

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics Simulation")

# Define colors
white = (255, 255, 255)
circle_color = (0, 0, 255)  # Blue

# Circle properties
# circle_radius = 20


class Circle:
    id_counter = 0  # Class variable to keep track of id

    id: int  # New id variable

    mass: float
    radius: float
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0

    def __init__(self, mass, radius, x, y, vx=0.0, vy=0.0):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.id = Circle.id_counter  # Assign the current id_counter value to the id
        Circle.id_counter += 1  # Increment id_counter for the next instance

    def apply_force(self, force, timedelta):
        fx, fy = force
        self.vx += fx / self.mass * timedelta
        self.vy += fy / self.mass * timedelta


circles = [
    Circle(mass=1, radius=10 * math.sqrt(1), x=width / 6, y=height / 2),
    Circle(mass=2, radius=10 * math.sqrt(2), x=2 * width / 6, y=height / 2),
    Circle(mass=3, radius=10 * math.sqrt(3), x=3 * width / 6, y=height / 2),
    Circle(mass=4, radius=10 * math.sqrt(4), x=4 * width / 6, y=height / 2),
    Circle(mass=5, radius=10 * math.sqrt(5), x=5 * width / 6, y=height / 2),
    Circle(mass=50, radius=10 * math.sqrt(5), x=width / 2, y=height / 2),
    Circle(mass=1, radius=10 * math.sqrt(1), x=width / 4, y=height / 2, vx=0, vy=100),
    *(
        Circle(
            mass=1,
            radius=10 * math.sqrt(1),
            x=width / 2 + width / 4 * math.cos(2 * math.pi * t / 10),
            y=height / 2 + width / 4 * math.sin(2 * math.pi * t / 10),
        )
        for t in range(3)
    ),
]


def elastic_collision(m_1, m_2, v_1i, v_2i):
    v_1f = (m_1 * v_1i + m_2 * v_2i - m_2 * (2 * m_1 * v_1i - m_1 * v_2i + m_2 * v_2i) / (m_1 + m_2)) / m_1
    v_2f = (2 * m_1 * v_1i - m_1 * v_2i + m_2 * v_2i) / (m_1 + m_2)
    return v_1f, v_2f


def inelastic_collision(m_1, m_2, v_1i, v_2i):
    v_1f = (m_1 * v_1i + m_2 * v_2i) / (m_1 + m_2)
    v_2f = (m_1 * v_1i + m_2 * v_2i) / (m_1 + m_2)
    return v_1f, v_2f


def percent_inelastic_collision(m_1, m_2, v_1i, v_2i, percent):
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
    force_amt = 40
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
    G = 8.0e3  # change this to change gravity
    for other_circle in circles:
        if other_circle is not circle:
            # Update velocity based on gravity
            combined_radius = circle.radius + other_circle.radius
            distance = sps.distance.euclidean((circle.x, circle.y), (other_circle.x, other_circle.y))
            r = max(distance, combined_radius)  # prevent division by zero
            F_g = G * circle.mass * other_circle.mass / r**2
            theta = np.arctan2(circle.y - other_circle.y, circle.x - other_circle.x)
            circle.apply_force((-F_g * np.cos(theta), -F_g * np.sin(theta)), timedelta)

            # Update velocity based on collisions
            if (circle.id < other_circle.id) and (
                # combined_radius - distance < 1
                True
            ):  # only check each pair of circles once
                if distance < combined_radius:
                    # Collision has occurred
                    # use both conservation of momentum and conservation of kinetic energy
                    v1x, v2x = elastic_collision(circle.mass, other_circle.mass, circle.vx, other_circle.vx)
                    v1y, v2y = elastic_collision(circle.mass, other_circle.mass, circle.vy, other_circle.vy)

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


# Set up the clock to control the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get elapsed time since the last frame
    timedelta = clock.tick(60) / 1000.0  # Assuming a target frame rate of 60 fps

    # Physics calculations for each circle
    for circle in circles:
        update_physics(circle, timedelta, circles)

    # Clear the screen
    screen.fill(white)

    # Draw circles
    for circle in circles:
        pygame.draw.circle(screen, circle_color, (int(circle.x), int(circle.y)), circle.radius)

    # Update the display
    pygame.display.flip()
