from model.cube import RubicsCube,Rotator
from model.scrambler import Scrammbler
from model.scramble_configurations import scramble_configurations
import numpy as np
import time
import copy
from search import Search

def solve_cube(scramble_size):
    #Initialise the Cube State - intial state is solved.
    cube = RubicsCube(size=3)
    #cubeSolver = CubeSolver()
    print(cube)

    #Scramble the state based on the preset configurations
    scrammbler = Scrammbler()
    scramble_sequence,unscramble_sequence = scrammbler.scramble(scramble_configurations[scramble_size])

    #Scramble a fresh cube to get a initial state
    cube.scramble(action_sequence=scramble_sequence)
    print(cube)

    # #Test
    # cube.scramble(action_sequence=unscramble_sequence)
    # print(cube)

    # """Further Steps:
    #     1. Take the scrambled state of the cube as intial state
    #     2. Find the steps to solve the cube
    #     3. Ideally, the result from step 2 should be unscrambled sequence
    # """

    searcher = Search(cube)
    #searcher.bfs()
    #searcher.dfs()
    # searcher.iddfs()
    searcher.astarsearch()

for size in range(7):
    print(f"Generating Scrambling sequence of size: {size+1}")
    solve_cube(size)
    print("="*50)