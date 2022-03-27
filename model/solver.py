from model.cube import RubicsCube,CubeSolver
from model.scrambler import Scrammbler
from model.scramble_configurations import scramble_configurations

#Initialise the Cube State - intial state is solved.
cube = RubicsCube()
cube.PrintCube()

#Scramble the state based on the preset configurations
scrammbler = Scrammbler()
scramble_sequence,unscramble_sequence = scrammbler.scramble(scramble_configurations[0])

#Scramble a fresh cube to get a initial state
cube.scramble(action_sequence=scramble_sequence)
cube.PrintCube()

#Test
cube.scramble(action_sequence=unscramble_sequence)
cube.PrintCube()

# """Further Steps:
#     1. Take the scrambled state of the cube as intial state
#     2. Find the steps to solve the cube
#     3. Ideally, the result from step 2 should be unscrambled sequence
# """



