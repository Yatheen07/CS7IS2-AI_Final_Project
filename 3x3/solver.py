from cube import RubicsCube,CubeSolver
from scrambler import Scrammbler
from scramble_configurations import scramble_configurations
import numpy as np
import time
import copy
from generate_patterns import *
from search import Search
#Initialise the Cube State - intial state is solved.
cube = RubicsCube()
cubeSolver = CubeSolver()
print(cube)

#Scramble the state based on the preset configurations
scrammbler = Scrammbler()
scramble_sequence,unscramble_sequence = scrammbler.scramble(scramble_configurations[0])

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

searcher = Search(cube,depth=10000)
searcher.bfs()
searcher.dfs()
searcher.iddfs()