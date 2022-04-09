import numpy as np

config_2x2 = np.array([
    ['W', 'W'],
    ['W', 'W'],
    ['G', 'G'],
    ['G', 'G'],
    ['R', 'R'],
    ['R', 'R'],
    ['B', 'B'],
    ['B', 'B'],
    ['O', 'O'],
    ['O', 'O'],
    ['Y', 'Y'],
    ['Y', 'Y'],
])

config_3x3 = np.array([
    ['W', 'W', 'W'],
    ['W', 'W', 'W'],
    ['W', 'W', 'W'],
    ['G', 'G', 'G'],
    ['G', 'G', 'G'],
    ['G', 'G', 'G'],
    ['R', 'R', 'R'],
    ['R', 'R', 'R'],
    ['R', 'R', 'R'],
    ['B', 'B', 'B'],
    ['B', 'B', 'B'],
    ['B', 'B', 'B'],
    ['O', 'O', 'O'],
    ['O', 'O', 'O'],
    ['O', 'O', 'O'],
    ['Y', 'Y', 'Y'],
    ['Y', 'Y', 'Y'],
    ['Y', 'Y', 'Y']
])

def get_solved_config(size):
    return config_2x2 if size == 2 else config_3x3
