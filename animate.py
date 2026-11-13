import imageio
import pygame
import numpy


def animate_surfaces(surfaces: list[pygame.Surface], video_path: str) -> None:
    """
    Convert a list of Pygame surfaces into an MP4 video.

    Args:
        surfaces (list[pygame.Surface]):
            A sequence of frames to encode.
        video_path (str):
            Output path for the video file (e.g., "output/jupiter_moons.mp4").

    The video is written using H.264 encoding at 10 FPS.
    """
    writer = imageio.get_writer(video_path, fps=10, codec='libx264', quality=8)

    for surface in surfaces:
        frame = pygame_surface_to_numpy(surface)
        writer.append_data(frame)

    writer.close()


def pygame_surface_to_numpy(surface: pygame.Surface) -> numpy.ndarray:
    """
    Convert a Pygame Surface to a NumPy RGB image array.

    Returns:
        numpy.ndarray: The frame as (height, width, 3) uint8 RGB.
    """
    return pygame.surfarray.array3d(surface).swapaxes(0, 1)
