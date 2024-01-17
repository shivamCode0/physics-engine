import math
from engine import Circle


width, height = 800, 600  # width and height of the screen
G = 8.0e0  # constant of universal gravitation
force_amt = 40  # amount of force to apply to the circle when arrow keys are pressed

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
