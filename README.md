# Physics Simulation using Pygame

Welcome to the Simple Physics Engine project! This is a simple physics engine implemented in Python using classical algebra-based physics and the Pygame library. The simulation features circles that interact with each other through gravity and elastic collisions. Below is a brief overview of the project components and how to use the simulation.

## Project Structure:

- **main.py:** The main Python script containing the physics simulation loop and user input handling.
- **Circle Class:** Defines the Circle class with attributes such as mass, radius, position, and velocity. Handles forces and collisions.
- **Collision Functions:** Includes functions for elastic collisions, inelastic collisions, and a weighted combination of both.
- **Update Physics Function:** Updates the physics of each circle based on user input, gravity, and collisions.
- **Pygame Setup:** Initializes the Pygame window, sets up colors, and defines the main game loop.
- **Gravity and Collision Physics:** Updates the velocity of circles based on gravitational forces and handles collisions between circles.
- **Pygame Drawing:** Clears the screen and draws circles with updated positions.

## How to Run the Simulation:

1. Make sure you have Python and Pygame installed on your system.
2. Execute the `main.py` script to launch the simulation.
3. Use the arrow keys to apply forces to the circles and observe their interactions.
4. Close the simulation window to exit.

## Circle Class:

The `Circle` class is a data structure representing individual circles in the simulation. Each circle has its own mass, radius, position, and velocity. The class also includes methods for applying forces and updating its state.

## Physics Formulas:

- **Gravity:** The simulation incorporates a simple gravitational force between circles based on Newton's law of gravitation.
- **Collisions:** The simulation supports both elastic and inelastic collisions between circles.
  - **Perfectly elastic collisions** are calculated using formulas that conserve both momentum and kinetic energy.
  - **Perfectly inelastic collisions** are also supported, where momentum is conserved, but kinetic energy may not be.
  - **Partially elastic collisions** are also supported, where the elasticity is dependent on a user-defined coefficient of elasticity.

## User Input:

- Use the arrow keys to apply forces to the circles. The simulation responds to left, right, up, and down arrow keys.

## Customization:

- Adjust the initial setup of circles in the `circles` list, changing their mass, radius, and initial positions.

## Notes:

- The simulation is configured to run at a target frame rate of 60 fps.

Feel free to explore the code, experiment with different parameters, and extend the project according to your preferences. Happy simulating!
