# main_controller.py
from dataclasses import dataclass
import pygame
import sys
import math
from engine import *
from config import *


class PhysicsSimulation:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Physics Simulation")

        # Define colors
        self.white = (255, 255, 255)
        self.circle_color = (0, 0, 255)  # Blue

        # Set up the clock to control the frame rate
        self.clock = pygame.time.Clock()

        # Create circles for the simulation
        self.circles = circles

        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_physics(self, timedelta):
        for circle in self.circles:
            update_physics(circle, timedelta, self.circles)

    def draw_circles(self):
        self.screen.fill(self.white)
        for circle in self.circles:
            pygame.draw.circle(self.screen, self.circle_color, (int(circle.x), int(circle.y)), circle.radius)

    def draw_fps(self, fps):
        fps_text = self.font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
        self.screen.blit(fps_text, (10, 10))

    def run_simulation(self):
        while True:
            self.handle_events()

            # Get elapsed time since the last frame
            timedelta = self.clock.tick(60) / 1000.0  # Assuming a target frame rate of 60 fps

            self.update_physics(timedelta)
            self.draw_circles()

            # Draw FPS counter
            fps = self.clock.get_fps()
            self.draw_fps(fps)

            # Update the display
            pygame.display.flip()


if __name__ == "__main__":
    simulation = PhysicsSimulation()
    simulation.run_simulation()
