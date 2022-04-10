from src.MCTS import MCTS
from src.cube import cube
from src.model import RL
import torch
import numpy as np

device = torch.device("cpu")

# This parameters should not be changed
INPUT_SIZE = [7, 24]
ACTIONS = 6

# Build solver network and feed state dict
net = RL(INPUT_SIZE, ACTIONS).to(device)
# Load the trained network
net.load_state_dict(torch.load('./trained_network.pt'))

# Initialize a cube
myCube = cube()


# Do some turns
# self.ACTIONS={0:"F", 1:"R", 2:"D", 3:"f", 4:"r", 5:"d"}

def get_action(move):
    if move < 3:
        counter = move + 3
    else:
        counter = move - 3
    return counter


# Scramble the cube
for i in range(20):
    action = np.random.randint(6)
    print('Scrambling move: {}'.format(myCube.ACTIONS[action]))
    myCube.turn(action)

    # Here we start solving!!!
    # Reset fail_cnt

fail_cnt = 0
solver = MCTS(myCube, net)

moves = []

while not myCube.check(myCube.state):
    while solver.search_cnt < solver.max_search:
        solver.add_leaves()
        solver.search()

    if len(solver.best_path) == 0:
        # We did not get anything
        fail_cnt += 1
        if fail_cnt > 5:
            print('Failed!')
            break
        if len(solver.best_node.lastActions) == 0:
            # If we did not EVEN find a best node
            action = np.random.randint(6)
        else:
            action = solver.best_node.lastActions[0]
        myCube.turn(action)
        del solver
        solver = MCTS(myCube, net)
        moves = moves + [action]
    else:
        # We find the way
        moves = moves + solver.best_path
        break

for i in range(len(moves)):
    print('The {} solve step is: {}'.format(i, myCube.ACTIONS[int(moves[i])]))
