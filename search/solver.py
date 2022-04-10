from model.cube import RubicsCube, Rotator
from model.scrambler import Scrammbler
from model.scramble_configurations import get_scramble_config
import numpy as np
import time
import copy
from search import Search


def solve_cube(scramble_size):
    # Initialise the Cube State - intial state is solved.
    wins = 0
    game_summary = []
    for i in range(10):
        game = {}
        cube = RubicsCube(size=3)

        # Scramble the state based on the preset configurations
        scrammbler = Scrammbler()
        scramble_sequence, unscramble_sequence = scrammbler.scramble(
            get_scramble_config(scramble_size)
        )

        # Scramble a fresh cube to get a initial state
        cube.scramble(action_sequence=scramble_sequence)

        searcher = Search(cube)
        goal_reached, path, time_elapsed, number_of_states = searcher.bfs()
        # goal_reached, path, time_elapsed, number_of_states = searcher.dfs()
        # goal_reached, path, time_elapsed, number_of_states = searcher.astarsearch()
        if goal_reached:
            wins += 1
        game["name"] = f"Game {i+1}"
        game["result"] = "Won" if goal_reached else "Lost"
        game["elapsed_time"] = time_elapsed
        game["Number of States Explored"] = number_of_states
        game_summary.append(game)
        print("=" * 75)

    for game in game_summary:
        print(
            f"[INFO] {game['name']} completed in {game['elapsed_time']}, Result: {game['result']}"
        )
    print(f"Win Percentage: {(wins/len(game_summary))*100}")
    print("=" * 75)


for size in range(1, 6):
    print(f"Generating Scrambling sequence of size: {size+1}")
    solve_cube(size)
    print("=" * 50)
