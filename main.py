"""
CLI entry point for the gravity simulation.

Usage:
    python main.py <scenario_name> <num_gens> <time_step> <canvas_width> <drawing_frequency>

Example:
    python main.py jupiter_moons 1000 60 1500 10

This will read:   data/jupiter_moons.txt
and write video:  output/jupiter_moons.mp4
"""

import sys
import pygame
from custom_io import read_universe
from gravity import simulate_gravity
from drawing import animate_system
from animate import animate_surfaces

def main():
    print("Building a gravity simulator.")

    if len(sys.argv) != 6:
        raise ValueError("Need 5 input parameters.")

    scenario = sys.argv[1]
    num_gens = int(sys.argv[2])
    time_step = float(sys.argv[3])
    canvas_width = int(sys.argv[4])
    drawing_frequency = int(sys.argv[5])

    input_file = f"data/{scenario}.txt"

    initial_universe = read_universe(input_file)

    print("File read. Simulate gravity.")

    time_points = simulate_gravity(initial_universe, num_gens, time_step)

    print("Gravity simulated. Now drawing files.")

    surfaces = animate_system(time_points, canvas_width, drawing_frequency)

    print("Surfaces drawn. Now generating video.")

    animate_surfaces(surfaces, f"output/{scenario}.mp4")

    print("Video generated. Success!")

if __name__ == "__main__":
    main()
