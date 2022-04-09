import numpy as np


TOP = 'W'
LEFT = 'G'
FRONT = 'R'
RIGHT = 'B'
BACK = 'O'
BOTTOM = 'Y'
FACES_LIST = [TOP, LEFT, FRONT, RIGHT, BACK, BOTTOM]

def get_solved_config(size):
    config = []
    for face in FACES_LIST:
        config.extend([[face]*size] * size)
    return np.array(config)
