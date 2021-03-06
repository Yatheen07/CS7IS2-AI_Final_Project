# check number of pieces on each side of cube that match color
# of the middle piece of that side
import random

from cube import Cube


def count_correct_side(state):
    correct = 0
    for side in state.__sides__:
        # get middle piece
        color = side[int(state.size / 2)][int(state.size / 2)]
        # subtract 1 to ignore middle cube
        correct -= 1
        for row in side:
            # filter items in each row that equal middle color
            # and add length of filtered list to total sum
            correct += row.count(color)
    return correct


def count_solved_sides(state):
    solved = 0
    for side in state.__sides__:
        color = side[0][0]
        # if number of pieces on this side equal to first square
        # is number of total pieces, side is solved
        if sum(row.count(color) for row in side) == state.size ** 2:
            solved += 1

    return solved


def count_crosses(state):
    crosses = 0
    for side in state.__sides__:
        color = side[1][1]
        if side[0][1] == color and side[1][0] == color and side[1][2] == color and side[2][1] == color:
            crosses += 1
    return crosses


def count_plus(state):
    xs = 0
    for side in state.__sides__:
        color = side[1][1]
        if side[0][0] == color and side[0][2] == color and side[2][0] == color and side[2][2] == color:
            xs += 1
    return xs


def scramble(n=5):
    c = Cube()
    return do_shuffle(c, n=n)


# def one_move_state():
#     c = Cube()
#     c.move(c.actions[0])
#     return c


def do_shuffle(cube, n=5):
    new_cube = cube.copy()
    for _ in range(n):
        new_cube = make_random_moves(new_cube)
    return new_cube


def make_random_moves(cube):
    action = random.choice(cube.actions)
    cube = make_rotations(cube, action)
    return cube


def make_rotations(s, action):
    new_state = s.copy()
    if action == 'left':
        new_state.turn_left()
    elif action == 'right':
        new_state.turn_right()
    elif action == 'front':
        new_state.turn_front()
    elif action == 'back':
        new_state.turn_back()
    elif action == 'top':
        new_state.turn_top()
    elif action == 'bottom':
        new_state.turn_bottom()
    new_state.__sides__ = [new_state.front(), new_state.back(), new_state.left(), new_state.right(), new_state.top(),
                           new_state.bottom()]
    return new_state
