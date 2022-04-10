import torch
import numpy as np

from src.cube import cube
from src.model import RL

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
DEPTH = 3
for i in range(DEPTH):
    action = np.random.randint(6)
    print('Scrambling move: {}'.format(myCube.ACTIONS[action]))
    myCube.turn(action)


def get_action(move):
    if move < 3:
        counter = move + 3
    else:
        counter = move - 3
    return counter


old_move = 99

# Solve only by using neural network
while not myCube.check(myCube.state):
    # policy_predict, value_predict = net.predict_cube(mycube)
    # You can use state instead of cube
    policy_predict, value_predict = net.predict_state(myCube.state)

    if old_move != 99:
        policy_predict[get_action(old_move)] = -99

    _, max_act_t = policy_predict.max(dim=0)
    action = max_act_t.numpy()
    old_move = action
    print(myCube.ACTIONS[int(action)])
    myCube.turn(action)
pass
