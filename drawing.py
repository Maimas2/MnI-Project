"""
Rendering helpers for animating a Universe with pygame.
"""

import math
import pygame
from animate import animate_surfaces, pygame_surface_to_numpy
from datatypes import Body, OrderedPair, Universe


# Drawing functions

def animate_system(
    time_points: list[Universe],
    canvas_width: int,
    drawing_frequency: int
) -> list[pygame.Surface]:
    """
    Render selected frames of the system into pygame surfaces.

    Frames are sampled every `drawing_frequency` simulation steps; trail history
    is updated more frequently using `TRAIL_FREQUENCY` so trails look smooth.

    Args:
        time_points: Snapshots of the Universe over time (0..N).
        canvas_width: Width/height (px) of the square canvas.
        drawing_frequency: Draw a frame when i % drawing_frequency == 0.

    Returns:
        A list of pygame.Surface objects (one per drawn frame).
    """
    if not isinstance(time_points, list):
        raise TypeError("time_points must be a list of Universe objects")
    if len(time_points) == 0:
        raise ValueError("time_points must not be empty")

    for u in time_points:
        if not isinstance(u, Universe):
            raise TypeError("all elements of time_points must be Universe objects")

    if not isinstance(canvas_width, int) or canvas_width <= 0:
        raise ValueError("canvas_width must be a positive integer")
    if not isinstance(drawing_frequency, int) or drawing_frequency <= 0:
        raise ValueError("drawing_frequency must be a positive integer")

    pygame.init()

    # Update trails every step; only render a surface every drawing_frequency steps
    TRAIL_FREQUENCY = 1
    trails: dict[int, list[OrderedPair]] = {i: [] for i in range(len(time_points[0].bodies))}
    surfaces: list[pygame.Surface] = []

    for i, u in enumerate(time_points):
        if i % TRAIL_FREQUENCY == 0:
            for idx, b in enumerate(u.bodies):
                trails[idx].append(OrderedPair(b.position.x, b.position.y))

        if i % drawing_frequency == 0:
            surfaces.append(draw_to_canvas(u, canvas_width, trails))

    pygame.quit()
    return surfaces

def draw_to_canvas(
    u: Universe,
    canvas_width: int,
    trails: dict[int, list[OrderedPair]],
) -> pygame.Surface:
    """
    Draw a single Universe snapshot onto a new pygame Surface.
    """
    # --- lightweight parameter checks ---
    if not isinstance(u, Universe):
        raise TypeError("u must be a Universe")
    if not isinstance(canvas_width, int) or canvas_width <= 0:
        raise ValueError("canvas_width must be a positive integer")
    if not isinstance(trails, dict):
        raise TypeError("trails must be a dict[int, list[OrderedPair]]")

    scale = canvas_width / u.width

    surface = pygame.Surface((canvas_width, canvas_width))
    surface.fill((0, 0, 0))  # black background

    # Draw trails
    for idx, trail in trails.items():
        color = (u.bodies[idx].red, u.bodies[idx].green, u.bodies[idx].blue)
        for pos in trail:
            px = int(pos.x * scale)
            py = int(pos.y * scale)
            if 0 <= px < canvas_width and 0 <= py < canvas_width:
                pygame.draw.circle(surface, color, (px, py), 1)

    # Draw bodies
    for b in u.bodies:
        px = int(b.position.x * scale)
        py = int(b.position.y * scale)
        radius = max(2, int(b.radius * scale))
        pygame.draw.circle(surface, (b.red, b.green, b.blue), (px, py), radius)

    return surface
