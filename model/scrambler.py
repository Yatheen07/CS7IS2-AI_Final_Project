import numpy as np
from .cube import Rotator

class Scrammbler:
    def __init__(self):
        self.action_map = {
            "F" : getattr(Rotator,"front_clockwise"),
            "L" : getattr(Rotator,"left_clockwise"),
            "R" : getattr(Rotator,"right_clockwise"),
            "D" : getattr(Rotator,"down_clockwise"),
            "U" : getattr(Rotator,"up_clockwise"),
            "B" : getattr(Rotator,"back_clockwise"),
            "F'" : getattr(Rotator,"front_anti_clockwise"),
            "L'" : getattr(Rotator,"left_anti_clockwise"),
            "R'" : getattr(Rotator,"right_anti_clockwise"),
            "D'" : getattr(Rotator,"down_anti_clockwise"),
            "U'" : getattr(Rotator,"up_anti_clockwise"),
            "B'" : getattr(Rotator,"back_anti_clockwise"),
        }
        self.rotations = {
            "F" : getattr(Rotator,"front_clockwise"),
            "L" : getattr(Rotator,"left_clockwise"),
            "R" : getattr(Rotator,"right_clockwise"),
            "D" : getattr(Rotator,"down_clockwise"),
            "U" : getattr(Rotator,"up_clockwise"),
            "B" : getattr(Rotator,"back_clockwise"),
            # "F'" : getattr(Rotator,"front_anti_clockwise"),
            # "L'" : getattr(Rotator,"left_anti_clockwise"),
            # "R'" : getattr(Rotator,"right_anti_clockwise"),
            # "D'" : getattr(Rotator,"down_anti_clockwise"),
            # "U'" : getattr(Rotator,"up_anti_clockwise"),
            # "B'" : getattr(Rotator,"back_anti_clockwise"),
        }
        self.negate_action = {
            "F" : "F'",
            "L" : "L'",
            "R" : "R'",
            "D" : "D'",
            "U" : "U'",
            "B" : "B'",
            "F'" : "F",
            "L'" : "L",
            "R'" : "R",
            "D'" : "D",
            "U'" : "U",
            "B'" : "B",
        }

    def get_scramble_action_sequence(self,scramble_string):
        scramble_sequence = []
        actions = scramble_string.split(" ")
        print(f"Scramble Sequence: {actions}")
        for action in actions:
            if action not in self.action_map:
                scramble_sequence.append(self.action_map[action[:-1]])
                scramble_sequence.append(self.action_map[action[:-1]])
            else:
                scramble_sequence.append(self.action_map[action])
        return scramble_sequence
    
    def get_unscramble_action_sequence(self,scramble_string):
        unscramble_sequence = []
        actions = reversed(scramble_string.split(" "))
        unscramble_actions = []
        for action in actions:
            if action not in self.action_map:
                negateAction = self.negate_action[action[:-1]]
                unscramble_sequence.append(self.action_map[negateAction])
                unscramble_sequence.append(self.action_map[negateAction])
                unscramble_actions.append(negateAction)
            else:
                negateAction = self.negate_action[action]
                unscramble_sequence.append(self.action_map[negateAction])
            unscramble_actions.append(negateAction)
        print(f"Unscramble Sequence: {unscramble_actions}")
        return unscramble_sequence

    def scramble(self,scramble_string):
        scramble_sequence = self.get_scramble_action_sequence(scramble_string)
        unscramble_sequence = self.get_unscramble_action_sequence(scramble_string)
        return scramble_sequence,unscramble_sequence