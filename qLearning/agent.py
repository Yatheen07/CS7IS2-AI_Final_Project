from cube import Cube
from utils import *


class Agent:
    def __init__(self, q_values=None, cube=None):
        self.count_visited = {}
        self.revisits = 0

        self.alpha = 0.6

        self.qValues = q_values if q_values is not None else {}

        self.R = {}

        self.start_state = cube if cube is not None else scramble(n=3)
        print("Start State:", self.start_state)

        self.current_state = self.start_state
        self.prev_prev_action = None
        self.actions = self.start_state.actions

        self.patterns = []
        self.last_action = None
        self.move = {
            "front": 0,
            "back": 0,
            "left": 0,
            "right": 0,
            "top": 0,
            "bottom": 0,
        }

    def register_patterns(self, levels=6):
        s = Cube()

        for action in self.actions:
            s_ = make_rotations(s, action)
            self.patterns.append(s_)
            for action_ in self.actions:
                self.qValues[(s_.__hash__(), action_)] = -10 if action_ != action else 10

        for level in range(levels - 1, 0, -1):
            new_patterns = []
            for s in self.patterns:
                for action in self.actions:
                    s_ = make_rotations(s, action)
                    new_patterns.append(s_)
                    for action_ in self.actions:
                        self.qValues[(s_.__hash__(), action_)] = -level if action_ != action else level
            self.patterns = new_patterns

    def do_q_learning(self, discount=0.99, episodes=10, epsilon=0.9):
        max_states = -1

        self.current_state = self.current_state
        for i in range(episodes):
            num_states = 0

            saved_rewards = self.current_state.__hash__() in self.R.keys()
            if not saved_rewards:
                self.R[self.current_state.__hash__()] = []
            if not self.current_state.__hash__ in self.count_visited:
                self.count_visited[self.current_state.__hash__()] = 1
            else:
                self.count_visited[self.current_state.__hash__()] += 1
            vc = self.count_visited[self.current_state.__hash__()]

            for action in self.actions:
                if not (self.current_state.__hash__(), action) in self.qValues.keys():
                    self.qValues[(self.current_state.__hash__(), action)] = 0
                else:
                    self.revisits += 1
                    break
                if not saved_rewards:
                    self.R[self.current_state.__hash__()].append(
                        self.reward(self.current_state, action)
                    )
            if 100 in self.R[self.current_state.__hash__()]:
                break
            follow_policy = random.uniform(0, 1.0)

            if follow_policy > epsilon:

                best_action = None
                best_qv = -100000000
                for action in self.actions:
                    if (
                            self.qValues[(self.current_state.__hash__(), action)] > best_qv
                            and action != self.last_action
                            and action != self.prev_prev_action
                    ):
                        best_action = action
                        best_qv = self.qValues[(self.current_state.__hash__(), action)]
                if best_qv == 0:
                    best_action = random.choice(self.actions)
                    while best_action == self.last_action:
                        best_action = random.choice(self.actions)

                self.move[best_action] = self.move[best_action] + 1

                for action in self.actions:
                    current_qv = self.qValues[(self.current_state.__hash__(), action)]
                    reward = self.reward(self.current_state, action)
                    max_reward = self.max_reward(self.current_state, action)
                    self.qValues[
                        (self.current_state.__hash__(), action)
                    ] = current_qv + self.alpha * (
                            reward + (discount ** vc) * max_reward - current_qv
                    )

                self.current_state.make_rotations(best_action)
                self.current_state = self.current_state.copy()
                if self.current_state.is_goal_state():
                    break
                self.prev_prev_action = self.last_action
                self.last_action = best_action
            else:

                action = random.choice(self.actions)
                self.move[action] = self.move[action] + 1
                while action == self.last_action or action == self.prev_prev_action:
                    action = random.choice(self.actions)

                reward = 0
                for action in self.actions:
                    current_qv = self.qValues[(self.current_state.__hash__(), action)]
                    reward = self.reward(self.current_state, action)
                    max_reward = self.max_reward(self.current_state, action)
                    self.qValues[
                        (self.current_state.__hash__(), action)
                    ] = current_qv + self.alpha * (
                            reward + (discount ** vc) * max_reward - current_qv
                    )

                self.current_state.make_rotations(action)
                self.current_state = self.current_state.copy()
                self.prev_prev_action = self.last_action
                self.last_action = action
                if self.current_state.is_goal_state():
                    break
            max_states = max(num_states, max_states)
        return max_states

    def play(self):
        self.prev_prev_action = None
        self.last_action = None
        self.current_state = self.start_state

        for i in range(30):
            best_action = None
            best_qv = -100000000
            if not (self.current_state.__hash__(), self.actions[0]) in self.qValues.keys():
                best_action = random.choice(self.actions)
                while (
                        best_action == self.prev_prev_action
                        or best_action == self.last_action
                ):
                    best_action = random.choice(self.actions)
                for action in self.actions:
                    self.qValues[(self.current_state.__hash__(), action)] = 0

            else:
                for action in self.actions:
                    if self.qValues[(self.current_state.__hash__(), action)] > best_qv and (
                            action != self.last_action and action != self.prev_prev_action
                    ):
                        best_action = action
                        best_qv = self.qValues[(self.current_state.__hash__(), action)]

            self.current_state.make_rotations(best_action)
            self.prev_prev_action = self.last_action
            self.last_action = best_action

            if self.current_state.is_goal_state():
                print("AGENT REACHED A GOAL STATE!!!")

                print(self.current_state)
                return True
        return False

    def print_(self):

        x = 0
        y = 0
        for key in self.qValues.keys():
            if self.qValues[key] != 0:
                x += 1
            else:
                y += 1
        result = {"q_values_dictionary": str(x + y), "q_values_zero": str(y), "q_values_non_zero": str(x),
                  "revisited_states": str(self.revisits)}
        return result

    def reward(self, state, action):

        next_state = make_rotations(state, action)
        if next_state.is_goal_state():
            return 100
        reward = -0.1
        solved_sides = 2 * (count_solved_sides(next_state) < count_solved_sides(state))
        solved_pieces = 0.5 * (
                count_correct_side(next_state) < count_correct_side(state)
        )
        if (next_state.__hash__(), action) in self.qValues.keys():
            reward -= 0.2
        reward -= solved_sides
        reward -= solved_pieces
        return reward

    def max_reward(self, state, action):
        new_state = make_rotations(state, action)
        if new_state not in self.R.keys():
            self.R[new_state] = []
            for action in self.actions:
                self.R[new_state].append(self.reward(new_state, action))
        return max(self.R[new_state])
