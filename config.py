import math
from Circle import Circle


width, height = 800, 600  # width and height of the screen
G = 2_00  # constant of universal gravitation
force_amt = 200  # amount of force to apply to the circle when arrow keys are pressed
C_R = 1  # coefficient of restitution for collisions
WALL_C_R = 0.8  # coefficient of restitution for collisions with the wall

circles = [
    Circle(mass=1, radius=10 * math.sqrt(1), pos=(width / 6, height / 2)),
    Circle(mass=2, radius=10 * math.sqrt(2), pos=(2 * width / 6, height / 2)),
    Circle(mass=3, radius=10 * math.sqrt(3), pos=(3 * width / 6, height / 2)),
    Circle(mass=4, radius=10 * math.sqrt(4), pos=(4 * width / 6, height / 2)),
    Circle(mass=5, radius=10 * math.sqrt(5), pos=(5 * width / 6, height / 2)),
    # Circle(mass=50, radius=10 * math.sqrt(5), pos=(width / 2, height / 2)),
    Circle(mass=1, radius=10 * math.sqrt(1), pos=(width / 4, height / 2), v=(0, 100)),
    *(
        Circle(
            mass=1,
            radius=10 * math.sqrt(1),
            pos=(
                width / 2 + width / 4 * math.cos(2 * math.pi * t / 10),
                height / 2 + width / 4 * math.sin(2 * math.pi * t / 10),
            ),
        )
        for t in range(10)
    ),
    *(
        Circle(
            mass=1,
            radius=10 * math.sqrt(1),
            pos=(
                width / 2 + width / 4 * 0.9 * math.cos(2 * math.pi * t / 10),
                height / 2 + width / 4 * 0.9 * math.sin(2 * math.pi * t / 10),
            ),
        )
        for t in range(10)
    ),
]
