import numpy as np
class RubicsCube:
    def __init__(self) -> None:
        self.solved_config = np.array([
            ['W', 'W', 'W'],
            ['W', 'W', 'W'],
            ['W', 'W', 'W'],
            ['G', 'G', 'G'],
            ['G', 'G', 'G'],
            ['G', 'G', 'G'],
            ['Y', 'Y', 'Y'],
            ['Y', 'Y', 'Y'],
            ['Y', 'Y', 'Y'],
            ['O', 'O', 'O'],
            ['O', 'O', 'O'],
            ['O', 'O', 'O'],
            ['R', 'R', 'R'],
            ['R', 'R', 'R'],
            ['R', 'R', 'R'],
            ['B', 'B', 'B'],
            ['B', 'B', 'B'],
            ['B', 'B', 'B'],
        ])
        self.cube = np.copy(self.solved_config)

    def is_cube_solved(self):
       return np.array_equal(self.cube,self.solved_config) 
    
    def PrintCube(self):
        print("             ", self.cube[0, 0:3])
        print("             ", self.cube[1, 0:3])
        print("             ", self.cube[2, 0:3])
        print(self.cube[3, 0:3], self.cube[6, 0:3], self.cube[9, 0:3], self.cube[12, 0:3])
        print(self.cube[4, 0:3], self.cube[7, 0:3], self.cube[10, 0:3], self.cube[13, 0:3])
        print(self.cube[5, 0:3], self.cube[8, 0:3], self.cube[11, 0:3], self.cube[14, 0:3])
        print("             ", self.cube[15, 0:3])
        print("             ", self.cube[16, 0:3])
        print("             ", self.cube[17, 0:3])
        print("="*25)

    def scramble(self,action_sequence):
        cubeSolver = CubeSolver()
        for action in action_sequence:
            action(cubeSolver,self.cube)
    
    def get_configuration_string(self):
        result = ""
        for row in range(18):
            result += ''.join(np.split(self.cube[row, 0:3],1)[0])
        return result


class CubeSolver:

    def front_clockwise(self,cube):
        #print("[INFO] Rotating front cube face in clockwise direction")
        cube[6:9, 0:3] = np.fliplr(cube[6:9, 0:3].transpose())
        temp1 = np.array(cube[2, 0:3])
        temp2 = np.array(cube[9:12, 0])
        temp3 = np.array(cube[15, 0:3])
        temp4 = np.array(cube[3:6, 2])
        cube[2, 0:3] = np.fliplr([temp4])[0]
        cube[9:12, 0] = temp1
        cube[15, 0:3] = np.fliplr([temp2])[0]
        cube[3:6, 2] = temp3
    
    def front_anti_clockwise(self,cube):
        #print("[INFO] Rotating front face in anti-clockwise direction")
        self.front_clockwise(cube)
        self.front_clockwise(cube)
        self.front_clockwise(cube)

    def up_clockwise(self,cube):  # action 3
        cube[0:3, 0:3] = np.fliplr(cube[0:3, 0:3].transpose())
        temp1 = np.array(cube[12, 0:3])
        temp2 = np.array(cube[9, 0:3])
        temp3 = np.array(cube[6, 0:3])
        temp4 = np.array(cube[3, 0:3])
        cube[12, 0:3] = temp4
        cube[9, 0:3] = temp1
        cube[6, 0:3] = temp2
        cube[3, 0:3] = temp3


    def up_anti_clockwise(self,cube):  # acion 4
        self.up_clockwise(cube)
        self.up_clockwise(cube)
        self.up_clockwise(cube)

    def down_clockwise(self,cube):  # action 5 Front down clock wise
        cube[15:18, 0:3] = np.fliplr(cube[15:18, 0:3].transpose())
        temp1 = np.array(cube[8, 0:3])
        temp2 = np.array(cube[11, 0:3])
        temp3 = np.array(cube[14, 0:3])
        temp4 = np.array(cube[5, 0:3])
        cube[8, 0:3] = temp4
        cube[11, 0:3] = temp1
        cube[14, 0:3] = temp2
        cube[5, 0:3] = temp3

    def down_anti_clockwise(self,cube):  # action 6
        self.down_clockwise(cube)
        self.down_clockwise(cube)
        self.down_clockwise(cube)

    def left_clockwise(self,cube): # action 7
        cube[3:6, 0:3] = np.fliplr(cube[3:6, 0:3].transpose())
        temp1 = np.array(cube[0:3, 0])
        temp2 = np.array(cube[6:9, 0])
        temp3 = np.array(cube[15:18, 0])
        temp4 = np.array(cube[12:15, 2])
        cube[0:3, 0] = np.fliplr([temp4])[0]
        cube[6:9, 0] = temp1
        cube[15:18, 0] = temp2
        cube[12:15, 2] = np.fliplr([temp3])[0]


    def left_anti_clockwise(self,cube):  # action 8
        self.left_clockwise(cube)
        self.left_clockwise(cube)
        self.left_clockwise(cube)


    def right_clockwise(self,cube):  # action 9 Front right clock wise
        cube[9:12, 0:3] = np.fliplr(cube[9:12, 0:3].transpose())
        temp1 = np.array(cube[0:3, 2])
        temp2 = np.array(cube[12:15, 0])
        temp3 = np.array(cube[15:18, 2])
        temp4 = np.array(cube[6:9, 2])
        cube[0:3, 2] = temp4
        cube[12:15, 0] = np.fliplr([temp1])[0]
        cube[15:18, 2] = np.fliplr([temp2])[0]
        cube[6:9, 2] = temp3


    def right_anti_clockwise(self,cube):  # action 10
        self.right_clockwise(cube)
        self.right_clockwise(cube)
        self.right_clockwise(cube)


    def back_clockwise(self,cube):  # action 11 Front  back clock wise
        cube[12:15, :] = np.fliplr(cube[12:15, :].transpose())
        temp1 = np.array(cube[0, 0:3])
        temp2 = np.array(cube[3:6, 0])
        temp3 = np.array(cube[17, 0:3])
        temp4 = np.array(cube[9:12, 2])
        cube[0, 0:3] = temp4
        cube[3:6, 0] = np.fliplr([temp1])[0]
        cube[17, 0:3] = temp2
        cube[9:12, 2] = np.fliplr([temp3])[0]

    def back_anti_clockwise(self,cube):  # action 12
        self.back_clockwise(cube)
        self.back_clockwise(cube)
        self.back_clockwise(cube)
