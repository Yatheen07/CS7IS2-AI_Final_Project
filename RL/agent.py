from model.config import FACES_LIST
from model.scrambler import Scrammbler
from model.cube import RubicsCube
import random
import copy
import numpy as np

class Patterns:
    def __init__(self,levels=8) -> None:
        self.qValues = {}
        self.rotations = Scrammbler().rotations.items()
        self.patterns = []
        cube = RubicsCube()
        for action,rotation in self.rotations:
            temp_cube = copy.deepcopy(cube)
            temp_cube.scramble([rotation])
            config_string = temp_cube.get_configuration_string()
            self.patterns.append(temp_cube)
            for action_,_ in self.rotations:
                self.qValues[(config_string,action_)] = -levels if action_ != action else levels

        for level in range(levels-1,0,-1):
            new_patterns = []
            for cube in self.patterns:
                for action,rotation in self.rotations:
                    cube.scramble([rotation])
                    config_string = cube.get_configuration_string()
                    new_patterns.append(cube)
                    for action_,_ in self.rotations:
                        key = (config_string,action_)
                        self.qValues[key] = -level if action_ != action else level
            self.patterns = new_patterns


class Agent:
    def __init__(self,qValues,cube) -> None:
        self.visited = []
        self.visit_count = {}
        self.revisits = 0

        #Setting initial alpha to 0.6 [Hyperparameter]
        self.alpha = 0.6

        self.QV = qValues
        # maps a state to a list of rewards for executing each possible outcome
        # can index list of rewards using directional class constants
        self.R = {}

        self.start_state = cube
        self.curr_state = copy.deepcopy(self.start_state)
        self.prev_state = None
        self.second_last_action = None

        self.actions = Scrammbler().rotations.items()

        self.last_action = None

        self.move = {
            "F" : 0,
            "L" : 0,
            "R" : 0,
            "D" : 0,
            "U" : 0,
            "B" : 0,
            "F'" : 0,
            "L'" : 0,
            "R'" : 0,
            "D'" : 0,
            "U'" : 0,
            "B'" : 0,
        }

    def QLearn(self, discount=0.99, episodes=10, epsilon=0.9):
        # execute q learning for specified number of episodes
        self.curr_state = self.curr_state
        for i in range(episodes):
            saved_rewards = self.curr_state.get_configuration_string() in self.R.keys()
            if not saved_rewards:
                self.R[self.curr_state.get_configuration_string()] = []
            if not self.curr_state.get_configuration_string() in self.visit_count:
                self.visit_count[self.curr_state.get_configuration_string()] = 1
            else:
                self.visit_count[self.curr_state.get_configuration_string()] += 1
            vc = self.visit_count[self.curr_state.get_configuration_string()]
            # initialize Q-Values of 0 for all state action pairs
            # for the given, state, if they do not exist
            for action,rotation in self.actions:
                if not (self.curr_state.get_configuration_string(), action) in self.QV.keys():
                    self.QV[(self.curr_state.get_configuration_string(), action)] = 0
                else:
                    self.revisits += 1
                    break
                if not saved_rewards:
                    self.R[self.curr_state.get_configuration_string()].append(
                        self.reward(self.curr_state, action,rotation))
            if 100 in self.R[self.curr_state.get_configuration_string()]:
                #print("REACHED GOAL, END QLEARN ITERATION")
                return
            follow_policy = random.uniform(0, 1.0)
            #print("random value generated is " + str(follow_policy))
            # if random number is > epsilon, we must select best move
            # by the highest q-value
            if follow_policy > epsilon:
                #print("FOLLOWING POLICY")
                # for action,rotation in self.actions:
                #     # print("q value for action " + action +
                #     #       " from curr state is " +
                #     #       str(self.QV[(self.curr_state.get_configuration_string(), action)]))
                best_action = None
                best_rotation = None
                best_QV = -100000000
                for action,rotation in self.actions:
                    if self.QV[(
                            self.curr_state.get_configuration_string(), action
                    )] > best_QV and action != self.last_action and action != self.second_last_action:
                        best_action = action
                        best_rotation = rotation
                        best_QV = self.QV[(self.curr_state.get_configuration_string(), action)]
                if best_QV == 0:
                    best_action,best_rotation = random.choice(list(self.actions))
                    while best_action == self.last_action:
                        best_action,best_rotation = random.choice(list(self.actions))
                #print("actions chosen = " + best_action)
                self.move[best_action] = self.move[best_action] + 1
                # update Q-Value for current state and action chosen based on the current policy, by taking original Q-value, and adding
                # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # action on the new state, minus the original Q-Value
                #reward = self.reward(self.curr_state, best_action)
                #max_reward = self.max_reward(self.curr_state, best_action)
                #self.QV[(self.curr_state.get_configuration_string(), best_action)] = best_QV + self.alpha*(reward +\
                #                                         discount*max_reward - best_QV)
                for action,rotation in self.actions:
                    curr_QV = self.QV[(self.curr_state.get_configuration_string(), action)]
                    reward = self.reward(self.curr_state, action,rotation)
                    max_reward = self.max_reward(self.curr_state, action,rotation)
                    self.QV[(self.curr_state.get_configuration_string(), action)] = curr_QV + self.alpha*(reward +\
                                                         (discount**vc)*max_reward - curr_QV)
                # #print("new q value for " + best_action + " action is " +
                #       str(self.QV[(self.curr_state.get_configuration_string(), best_action)]))
                new_state = copy.deepcopy(self.curr_state)
                new_state.scramble([best_rotation])
                self.curr_state = new_state
                if self.curr_state.is_cube_solved():
                    # print("reached goal state while in Q-learning epsiode " +
                    #       str(i))
                    #time.sleep(2)
                    return
                self.second_last_action = self.last_action
                self.last_action = best_action
            else:
                # pick random move
                action,rotation = random.choice(list(self.actions))
                self.move[action] = self.move[action] + 1
                while action == self.last_action or action == self.second_last_action:
                    action,rotation = random.choice(list(self.actions))
                # # update Q-Value for current state and randomly chosen action, by taking original Q-value, and adding
                # # alpha times the reward value of the new state plus the discounted max_reward of executing every possible
                # # action on the new state, minus the original Q-Value
                # curr_QV = self.QV[(self.curr_state.get_configuration_string(), action)]
                # reward = self.reward(self.curr_state, action,rotation)
                # max_reward = self.max_reward(self.curr_state, action,rotation)
                # # print("max reward... " + str(max_reward))
                # # print("reward... " + str(reward))
                # self.QV[(self.curr_state.get_configuration_string(), action)] = curr_QV + self.alpha*(reward +\
                # (discount**vc)*max_reward - curr_QV)
                reward = 0
                for action,rotation in self.actions:
                    curr_QV = self.QV[(self.curr_state.get_configuration_string(), action)]
                    reward = self.reward(self.curr_state, action,rotation)
                    max_reward = self.max_reward(self.curr_state, action,rotation)
                    self.QV[(self.curr_state.get_configuration_string(), action)] = curr_QV + self.alpha*(reward +\
                                                         (discount**vc)*max_reward - curr_QV)

                #print(self.reward(self.curr_state,action))
                #print(self.QV[(self.curr_state,action)])
                new_state = copy.deepcopy(self.curr_state)
                new_state.scramble([rotation])
                self.curr_state = new_state
                self.second_last_action = self.last_action
                self.last_action = action
                if self.curr_state.is_cube_solved():
                    # print("reached goal state while in Q-learning epsiode " +
                    #       str(i))
                    #time.sleep(2)
                    return
    
    def Play(self,cube):
        self.second_last_action = None
        self.last_action = None
        self.curr_state = copy.deepcopy(cube)
        #print(self.curr_state)
        for i in range(30):
            best_action = None
            best_rotation = None
            best_QV = -100000000
            if not (self.curr_state.get_configuration_string(),
                    list(self.actions)[0]) in self.QV.keys():
                best_action,best_rotation = random.choice(list(self.actions))
                while best_action == self.second_last_action or best_action == self.last_action:
                    best_action,best_rotation = random.choice(list(self.actions))
                for action,rotation in self.actions:
                    self.QV[(self.curr_state.get_configuration_string(), action)] = 0
                best_QV = 0
            else:
                for action,rotation in self.actions:
                    if self.QV[(self.curr_state.get_configuration_string(), action)] > best_QV \
                    and (action != self.last_action and action != self.second_last_action):
                        best_action = action
                        best_rotation = rotation
                        best_QV = self.QV[(self.curr_state.get_configuration_string(), action)]
                #if best_QV == 0:
                #    best_action,rotation = random.choice(list(self.actions))
                #    while best_action == self.last_action or best_action == self.second_last_action:
                #        best_action,rotation = random.choice(list(self.actions))
            # print("actions chosen = " + best_action)
            # print("last action = " + (
            #     self.last_action if self.last_action is not None else "None"))
            # print("q value is " +
            #       str(self.QV[(self.curr_state.get_configuration_string(), best_action)]))
            #time.sleep(1)
            new_state = copy.deepcopy(self.curr_state)
            new_state.scramble([best_rotation])
            self.curr_state = new_state
            self.second_last_action = self.last_action
            self.last_action = best_action
            #print(self.curr_state)
            if self.curr_state.is_cube_solved():
                print("AGENT REACHED A GOAL STATE!!!")
                #time.sleep(5)
                return True
        return False

    def print_(self):
        #print("=============")
        x = 0
        y = 0
        for key in self.QV.keys():
            if self.QV[key] != 0:
                x += 1
            else:
                y += 1
        result = {}
        result["q_values_dictionary"] = str(x + y)
        result["q_values_zero"] = str(y)
        result["q_values_non_zero"] = str(x)
        result["revisited_states"] = str(self.revisits)
        return result
        # print("number of q values in dictionary is " + str(x + y))
        # print("number of q values with zero value is " + str(y))
        # print("number of q value with non zero value is " + str(x))
        # print("number of re visited states = " + str(self.revisits))
        #print(self.move)
            
    def reward(self, state, action,rotation):
        # this reward function should be a function approximation made up of
        # a set of features, these features should be in decreasing order of priority:
        # 1. solved sides ()
        # use next state to get value for next state vs. self.curr_state, to determine
        # if feature values should be 1 or 0, e.g. if solved_sides(next_state) > solved_sides(self.curr_state)
        # then the solved sides feature is 1, else 0
        temp_cube = copy.deepcopy(state)
        temp_cube.scramble([rotation])
        if temp_cube.is_cube_solved():
            # print(state)
            # print(next_state)
            # print("REWARD IS GOAL")
            return 100
        reward = -0.1
        solved_sides = 2 * (num_solved_sides(temp_cube) < num_solved_sides(temp_cube))
        solved_pieces = 0.5 * (num_pieces_correct_side(temp_cube) < num_pieces_correct_side(temp_cube))
        if (temp_cube.get_configuration_string(), action) in self.QV.keys():
            reward -= 0.2
        reward -= solved_sides
        reward -= solved_pieces
        return reward

    def max_reward(self, state, action,rotation):
        temp_cube = copy.deepcopy(state)
        temp_cube.scramble([rotation])
        if not temp_cube in self.R.keys():
            self.R[temp_cube] = []
            for action,rotation in self.actions:
                self.R[temp_cube].append(self.reward(temp_cube, action,rotation))
        return max(self.R[temp_cube])

def num_pieces_correct_side(cube):
    if cube.size == 2:
        return 0
    else:
        correct = 0
        for i in range(0, cube.size*6, cube.size):
            color = cube.cube[i+1,1]
            correct -= 1
            for row in range(3):
                correct += sum([1 if value == color else 0 for value in cube.cube[row,:]])
        return correct

def num_solved_sides(cube):
    solved = 0
    for i in range(0, cube.size*6, cube.size):
        if np.array_equal(
            cube.cube[i:i+cube.size, 0:cube.size],
            cube.solved_config[i:i+cube.size, 0:cube.size]
        ):
            solved += 1
    return solved

def num_crosses(cube):
    if cube.size == 2:
        return 0
    else:
        crosses = 0
        for i in range(0, cube.size*6, cube.size):
            vert = cube.cube[i:i+cube.size, 1]
            hori = cube.cube[i+1, 0:cube.size]
            if np.array_equal(vert, hori):
                crosses += 1
        return crosses
    
def num_xs(cube):
    if cube.size == 2:
        return num_solved_sides(cube)
    else:
        xs = 0
        for i in range(0, cube.size*6, cube.size):
            diag1 = np.array([cube.cube[i, 0],cube.cube[i+1, 1],cube.cube[i+2, 2]])
            diag2 = np.array([cube.cube[i, 2],cube.cube[i+1, 1],cube.cube[i+2, 0]])
            if np.array_equal(diag1, diag2):
                xs += 1
        return xs