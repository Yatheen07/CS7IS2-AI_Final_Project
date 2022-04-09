from collections import deque
import copy
import time
from cube import RubicsCube
import numpy as np
from scrambler import Scrammbler

class Search:

    def __init__(self,cube,depth=1000) -> None:
        self.cube = cube
        self.depth = depth
        self.rotations = Scrammbler().action_map.items()
        self.start_state_config = "START_STATE"
    
    def _trace_path(self, node, visited):
        path = []
        current_config,action = visited[node.get_configuration_string()]
        path.append(action)
        while current_config != self.start_state_config:
            current_config, action = visited[current_config]
            path.append(action)
        return path[::-1][1:]

    def traverse_states(self, frontier,pop_action):
        goal_reached = False
        visited = {self.cube.get_configuration_string(): (self.start_state_config,"-1")}
        currentNode = copy.deepcopy(self.cube)
        frontier.append(currentNode)
        while frontier:
            if self.depth == 0:
                break
            currentNode = pop_action(frontier)
            if currentNode.is_cube_solved():
                goal_reached = True
                break
            else:
                for action,rotation in self.rotations:
                    temp_cube = RubicsCube()
                    new_node = copy.deepcopy(currentNode)
                    new_node.scramble([rotation])
                    temp_cube.cube = new_node.cube

                    config_string = temp_cube.get_configuration_string()

                    if not config_string in visited:
                        visited[config_string] = (currentNode.get_configuration_string(), action)
                        frontier.append(temp_cube)
                    else:
                        continue

            self.depth -= 1
        return goal_reached,visited,currentNode

    def printResults(self,path,goal_reached,algorithm,time_elapsed):
        print(f"Unscrambling Rubics Cube using {algorithm}")
        print("--"*25)
        print(f"[INFO] Goal-Reached? {goal_reached}")
        if goal_reached:
            print(f"[INFO] Path: {path}")
        print(f"[INFO] Elapsed time: {time_elapsed}")
        print("--"*25)

    def bfs(self):
        start = time.time()
        frontier = deque()
        pop_action = getattr(deque,"popleft")
        goal_reached, visited, currentNode = self.traverse_states(frontier,pop_action)
        self.printResults(path=self._trace_path(currentNode,visited),goal_reached=goal_reached,algorithm="Breadth First Search",time_elapsed=time.time() - start)

    def dfs(self):
        start = time.time()
        frontier = list()
        pop_action = getattr(list,"pop")
        goal_reached, visited, currentNode = self.traverse_states(frontier,pop_action)
        self.printResults(path=self._trace_path(currentNode,visited),goal_reached=goal_reached,algorithm="Depth First Search",time_elapsed=time.time() - start)
    
    def iddfs(self):
        start = time.time()
        class CubeState:
            state = None
            parent = None
            action = None
            cost = 0

        goal_reached = False
        visited = {self.cube.get_configuration_string(): (self.start_state_config,"-1")}
        
        startState = CubeState()
        startState.state = self.cube
        
        cost_limit = 1
        nodes = 0
        frontier = list()
        branching_factors = list()
        currentState = copy.deepcopy(startState)
        while cost_limit<=self.depth:
            frontier.append(startState)
            while len(frontier) != 0:
                currentState = frontier.pop()
                
                if currentState.state.is_cube_solved():
                    print('[INFO] Goal Height:', currentState.cost)
                    print('[INFO] Branching Factor:', sum(branching_factors)/len(branching_factors))
                    print("[INFO] Nodes Generated:", nodes)
                    print(f"[INFO] Elapsed time: {time.time() - start}")
                    goal_reached = True
                    # self.printResults(path=self._trace_path(currentState.state,visited),goal_reached=goal_reached,algorithm="Iterative Deepning Depth First Search",time_elapsed=time.time() - start)
                    return

                if currentState.cost + 1 <= cost_limit:
                    child_cost = currentState.cost + 1
                    branch = 0

                    for key,action in self.rotations:
                        nodes = nodes + 1
                        new = CubeState()
                        new.state = copy.deepcopy(currentState.state)
                        new.cost = child_cost
                        new.parent = currentState
                        new.move = key
                        new.state.scramble([action])
                        
                        config_string = new.state.get_configuration_string()
                        frontier.append(new)
                        # if not config_string in visited:
                        #     visited[config_string] = (currentState.state.get_configuration_string(), key)
                        #     frontier.append(new)
                        #     branch += 1
                        # else:
                        #     continue
                    # if curr.parent is not None and np.array_equal(curr.parent.cube, new.cube):
                    if currentState.parent is not None and (self.commonParent(new.cube, currentState) or self.containsChild(new.cube, frontier)):
                        continue
                    frontier.append(new)
                    branch += 1
                    branching_factors.append(branch)

            branching_factors.clear()
            cost_limit = cost_limit + 1

        #self.printResults(path=self._trace_path(currentState.state,visited),goal_reached=goal_reached,algorithm="IDDFS",time_elapsed=time.time() - start)

    # checks if child ascendant of parent
    def commonParent(child, parent):
        curr = parent.parent
        while curr is not None:
            if np.array_equal(curr.cube, child): return True
            curr = curr.parent

        return False


    # checks if frontier contains child
    def containsChild(child, frontier):
        for curr in frontier:
            if np.array_equal(curr.cube, child): return True
        return False