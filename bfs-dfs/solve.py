from collections import deque

from cube import Cube

class TestCases:
    test_case1 = (6, 7, 8, 20, 18, 19, 3, 4, 5, 16, 17, 15, 0, 1, 2, 14, 12, 13, 10, 11, 9, 21, 22, 23)
    goal = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)

def bfs(source, goal):
    cube = Cube()
    visited = {}

    def trace_path():
        path = []
        temp = goal
        while temp != source:
            temp, rot = visited[temp_node]
            path.append(rot)
        return path[::-1]

    visited[source] = (source, -1)
    nodes = deque()
    nodes.append(source)
    while nodes:
        node = nodes.popleft()
        if node == goal:
            return trace_path()
        else:
            for rot in cube.rotations:
                temp_node = cube.apply_rotation(node, cube.rotations[rot])
                if not temp_node in visited:
                    visited[temp_node] = (node, rot)
                    nodes.append(temp_node)
                else:
                    continue

def main():
    path = bfs(TestCases.test_case1, TestCases.goal)
    print(path)

if __name__ == '__main__':
    main()
