from cube import CubeSolver, RubicsCube
from collections import deque
from scrambler import Scrammbler
import copy

class PatternGenerator:
    def __init__(self, source, depth):
        self.depth = depth
        self.states = []
        self.rotations = Scrammbler().action_map
        self.source = self.source1 = source
    
    def _trace_path(self, node, visited):
        path = []
        node.PrintCube()
        while node != self.source:
            node, rot = visited[node]
            # print(rot)
            # node.PrintCube()
            path.append(rot)
        return path[::-1]

    def _bfs(self):
        visited = {self.source: (self.source, -1)}

        nodes = deque()
        nodes.append(self.source)

        while nodes:
            if self.depth == 0:
                return node, visited
            node = nodes.popleft()
            if node.is_cube_solved():
                print(node.PrintCube())
                return node, visited
            else:
                for rot in self.rotations:
                    temp_cube = RubicsCube()
                    node_copy = copy.deepcopy(node)
                    node_copy.scramble([self.rotations[rot]])
                    temp_cube.cube = node_copy.cube

                    if not temp_cube in visited:
                        visited[temp_cube] = (node, rot)
                        nodes.append(temp_cube)
                    else:
                        continue
            self.depth -= 1
    
    def generate_pattern(self):
        self.source.PrintCube()
        node, visited = self._bfs()
        return self._trace_path(node, visited)
