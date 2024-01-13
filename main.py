from dataclasses import dataclass
import pygame
import sys
import numpy as np
import math

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


@dataclass
class Circle:
    mass: float
    radius: float
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0

    def apply_force(self, force, timedelta):
        fx, fy = force
        self.vx += fx / self.mass * timedelta
        self.vy += fy / self.mass * timedelta


# List to store circle properties
# circles = [
#     {"x": width // 4, "y": height // 2, "vx": 0, "vy": 0},
#     {"x": width // 2, "y": height // 2, "vx": 0, "vy": 0},
#     {"x": 3 * width // 4, "y": height // 2, "vx": 0, "vy": 0},
# ]
circles = [
    Circle(mass=1, radius=10 * math.sqrt(1), x=width / 4, y=height / 2),
    Circle(mass=2, radius=10 * math.sqrt(2), x=width / 2, y=height / 2),
    Circle(mass=3, radius=10 * math.sqrt(3), x=3 * width / 4, y=height / 2),
    # Circle(mass=50, radius=10 * math.sqrt(5), x=width / 2, y=height / 2),
    # # Circle(mass=1, radius=10 * math.sqrt(1), x=width / 4, y=height / 2, vx=0, vy=100),
    # *(
    #     Circle(
    #         mass=1,
    #         radius=5 * math.sqrt(1),
    #         x=width / 2 + width / 4 * math.cos(2 * math.pi * t / 100),
    #         y=height / 2 + width / 4 * math.sin(2 * math.pi * t / 100),
    #     )
    #     for t in range(10)
    # ),
]


# Function for physics calculations
# def update_physics(circle, timedelta, circles):
#     # Update velocity based on arrow key input
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         circle["vx"] -= 1
#     if keys[pygame.K_RIGHT]:
#         circle["vx"] += 1
#     if keys[pygame.K_UP]:
#         circle["vy"] -= 1
#     if keys[pygame.K_DOWN]:
#         circle["vy"] += 1

#     # Update position based on velocity and elapsed time
#     circle["x"] += circle["vx"] * timedelta
#     circle["y"] += circle["vy"] * timedelta


def update_physics(circle: Circle, timedelta: float, circles: list[Circle]):
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
            r = np.sqrt((circle.x - other_circle.x) ** 2 + (circle.y - other_circle.y) ** 2)
            F_g = G * circle.mass * other_circle.mass / r**2
            theta = np.arctan2(circle.y - other_circle.y, circle.x - other_circle.x)
            circle.apply_force((-F_g * np.cos(theta), -F_g * np.sin(theta)), timedelta)

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
