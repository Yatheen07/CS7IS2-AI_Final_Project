from collections import deque
import time
from cube import Cube


class TestCases:
    test_case1 = {
        'source': (6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23),
        'goal': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)
    }

def trace_path(visited, source, goal):
    path = []
    temp = goal
    while temp != source:
        temp, rot = visited[temp]
        path.append(rot)
    return path[::-1]

def search(source, goal, func='DFS'):
    cube = Cube()

    visited = {source: (source, -1)}

    nodes = deque()
    nodes.append(source)

    while nodes:
        if func == 'BFS':
            node = nodes.popleft()
        else:
            node = nodes.pop()
        if node == goal:
            print('Goal State Reached')
            return visited
        else:
            for rot in cube.rotations:
                temp_node = cube.apply_rotation(node, cube.rotations[rot])
                if not temp_node in visited:
                    visited[temp_node] = (node, rot)
                    nodes.append(temp_node)
                else:
                    continue

def solve(test_case, func):
    source = test_case['source']
    goal = test_case['goal']
    start = time.time()
    visited = search(source, goal, func)
    end = time.time()
    path = trace_path(visited, source, goal)
    print(f'The time taken to reach the goal state using {func}: {round(end - start, 2)}')
    if func == 'BFS':
        print(f'The path is: {path}')

def main():
    solve(TestCases.test_case1, 'BFS')
    solve(TestCases.test_case1, 'DFS')


if __name__ == '__main__':
    main()
