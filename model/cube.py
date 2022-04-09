import numpy as np
from .config import get_solved_config

class RubicsCube:
    def __init__(self, size=3):
        self.size = size
        self.solved_config = get_solved_config(size)
        self.cube = np.copy(self.solved_config)

    def is_cube_solved(self):
        return np.array_equal(self.cube, self.solved_config)

    def __str__(self):
        whitespace_count = self.size * 4 + 1
        s = ''

        for i in range(self.size):
            s += " " * whitespace_count + np.array_str(self.cube[i, 0:self.size]) + '\n'

        for i in range(self.size):
            s += np.array_str(self.cube[i + self.size, 0:self.size]) + \
                np.array_str(self.cube[i + (2 * self.size), 0:self.size]) +  \
                np.array_str(self.cube[i + (3 * self.size), 0:self.size]) +  \
                np.array_str(self.cube[i + (4 * self.size), 0:self.size]) + '\n'

        for i in range(self.size):
            s += " " * whitespace_count + np.array_str(self.cube[i + (5 * self.size), 0:self.size]) + '\n'

        return s
    
    def scramble(self, action_sequence):
        rotator = Rotator(self.cube, self.size)
        for action in action_sequence:
            action(rotator)
    
    def get_configuration_string(self):
        result = ""
        for row in range(self.size * 6):
            result += ''.join(np.split(self.cube[row, 0:self.size], 1)[0])
        return result

class Rotator:
    def __init__(self, cube, size):
        self.cube = cube
        self.size = size

    def front_clockwise(self):
        self.cube[self.size*2:self.size*3, 0:self.size] = np.fliplr(
            self.cube[self.size*2:self.size*3, 0:self.size].transpose()
        )

        temp1 = np.array(self.cube[self.size-1, 0:self.size])
        temp2 = np.array(self.cube[self.size*3:self.size*4, 0])
        temp3 = np.array(self.cube[self.size*5, 0:self.size])
        temp4 = np.array(self.cube[self.size:self.size*2, self.size-1])

        self.cube[self.size-1, 0:self.size] = np.fliplr([temp4])[0]
        self.cube[self.size*3:self.size*4, 0] = temp1
        self.cube[self.size*5, 0:self.size] = np.fliplr([temp2])[0]
        self.cube[self.size:self.size*2, self.size-1] = temp3

    def front_anti_clockwise(self):
        self.front_clockwise()
        self.front_clockwise()
        self.front_clockwise()
    
    def up_clockwise(self):
        self.cube[0:self.size, 0:self.size] = np.fliplr(
            self.cube[0:self.size, 0:self.size].transpose()
        )

        temp1 = np.array(self.cube[self.size*4, 0:self.size])
        temp2 = np.array(self.cube[self.size*3, 0:self.size])
        temp3 = np.array(self.cube[self.size*2, 0:self.size])
        temp4 = np.array(self.cube[self.size*1, 0:self.size])

        self.cube[self.size*4, 0:self.size] = temp4
        self.cube[self.size*3, 0:self.size]= temp1
        self.cube[self.size*2, 0:self.size]= temp2
        self.cube[self.size*1, 0:self.size]= temp3
    
    def up_anti_clockwise(self):
        self.up_clockwise()
        self.up_clockwise()
        self.up_clockwise()
    
    def down_clockwise(self):
        self.cube[self.size*5:self.size*6, 0:self.size] = np.fliplr(
            self.cube[self.size*5:self.size*6, 0:self.size].transpose()
        )

        temp1 = np.array(self.cube[self.size*3-1, 0:self.size])
        temp2 = np.array(self.cube[self.size*4-1, 0:self.size])
        temp3 = np.array(self.cube[self.size*5-1, 0:self.size])
        temp4 = np.array(self.cube[self.size*2-1, 0:self.size])

        self.cube[self.size*3-1, 0:self.size] = temp4
        self.cube[self.size*4-1, 0:self.size] = temp1
        self.cube[self.size*5-1, 0:self.size] = temp2
        self.cube[self.size*2-1, 0:self.size] = temp3

    def down_anti_clockwise(self):
        self.down_clockwise()
        self.down_clockwise()
        self.down_clockwise()
    
    def left_clockwise(self):
        self.cube[self.size:self.size*2, 0:self.size] = np.fliplr(
            self.cube[self.size:self.size*2, 0:self.size].transpose()
        )

        temp1 = np.array(self.cube[0:self.size, 0])
        temp2 = np.array(self.cube[self.size*2:self.size*3, 0])
        temp3 = np.array(self.cube[self.size*5:self.size*6, 0])
        temp4 = np.array(self.cube[self.size*4:self.size*5, self.size-1])

        self.cube[0:self.size, 0] = np.fliplr([temp4])[0]
        self.cube[self.size*2:self.size*3, 0] = temp1
        self.cube[self.size*5:self.size*6, 0] = temp2
        self.cube[self.size*4:self.size*5, self.size-1] = np.fliplr([temp3])[0]

    def left_anti_clockwise(self):
        self.left_clockwise()
        self.left_clockwise()
        self.left_clockwise()
    
    def right_clockwise(self):
        self.cube[self.size*3:self.size*4, 0:self.size] = np.fliplr(
            self.cube[self.size*3:self.size*4, 0:self.size].transpose()
        )

        temp1 = np.array(self.cube[0:self.size, self.size-1])
        temp2 = np.array(self.cube[self.size*4:self.size*5, 0])
        temp3 = np.array(self.cube[self.size*5:self.size*6, self.size-1])
        temp4 = np.array(self.cube[self.size*2:self.size*3, self.size-1])

        self.cube[0:self.size, self.size-1] = temp4
        self.cube[self.size*4:self.size*5, 0] = np.fliplr([temp1])[0]
        self.cube[self.size*5:self.size*6, self.size-1] = np.fliplr([temp2])[0]
        self.cube[self.size*2:self.size*3, self.size-1] = temp3

    def right_anti_clockwise(self):
        self.right_clockwise()
        self.right_clockwise()
        self.right_clockwise()
    
    def back_clockwise(self):
        self.cube[self.size*4:self.size*5, :] = np.fliplr(
            self.cube[self.size*4:self.size*5, :]
        )

        temp1 = np.array(self.cube[0, 0:self.size])
        temp2 = np.array(self.cube[self.size:self.size*2, 0])
        temp3 = np.array(self.cube[self.size*6-1, 0:self.size])
        temp4 = np.array(self.cube[self.size*3:self.size*4, self.size-1])

        self.cube[0, 0:self.size] = temp4
        self.cube[self.size:self.size*2, 0] = np.fliplr([temp1])[0]
        self.cube[self.size*6-1, 0:self.size] = temp2
        self.cube[self.size*3:self.size*4, self.size-1] = np.fliplr([temp3])[0]

    def back_anti_clockwise(self):
        self.back_clockwise()
        self.back_clockwise()
        self.back_clockwise()
