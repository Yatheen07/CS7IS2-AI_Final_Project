from collections import deque
import copy
import time
from model.cube import RubicsCube
import numpy as np
from model.scrambler import Scrammbler
import util
class Search:

    def __init__(self, rubicsCube, depth=None) -> None:
        self.rubicsCube = rubicsCube
        self.cube = self.rubicsCube.cube
        self.size = self.rubicsCube.size
        self.depth = depth
        self.rotations = Scrammbler().action_map.items()
        #self.rotations = Scrammbler().rotations.items()
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
        number_of_states = 0
        visited = {self.rubicsCube.get_configuration_string(): (self.start_state_config,"-1")}
        currentNode = copy.deepcopy(self.rubicsCube)
        frontier.append(currentNode)
        while frontier:
            if self.depth and self.depth == 0:
                break
            currentNode = pop_action(frontier)
            if currentNode.is_cube_solved():
                goal_reached = True
                break
            else:
                for action,rotation in self.rotations:
                    temp_cube = RubicsCube(self.size)
                    new_node = copy.deepcopy(currentNode)
                    new_node.scramble([rotation])
                    temp_cube.cube = new_node.cube

                    config_string = temp_cube.get_configuration_string()

                    if not config_string in visited:
                        visited[config_string] = (currentNode.get_configuration_string(), action)
                        frontier.append(temp_cube)
                    
                    if temp_cube.is_cube_solved():
                        print(temp_cube)
                        goal_reached = True
                        return goal_reached,visited,temp_cube,len(visited)-1

            if self.depth:
                self.depth -= 1
        return goal_reached,visited,currentNode,len(visited)-1

    def printResults(self,path,goal_reached,algorithm,time_elapsed,number_of_states):
        print(f"Unscrambling Rubics Cube using {algorithm}")
        print("--"*25)
        print(f"[INFO] Goal-Reached? {goal_reached}")
        if goal_reached:
            print(f"[INFO] Path: {path}")
        print(f"[INFO] Elapsed time: {time_elapsed}")
        print(f"[INFO] Number of States: {number_of_states}")
        print("--"*25)

    def bfs(self):
        start = time.time()
        frontier = deque()
        pop_action = getattr(deque,"popleft")
        goal_reached, visited, currentNode,number_of_states = self.traverse_states(frontier,pop_action)
        self.printResults(path=self._trace_path(currentNode,visited),goal_reached=goal_reached,algorithm="Breadth First Search",time_elapsed=time.time() - start,number_of_states=number_of_states)

    def dfs(self):
        start = time.time()
        frontier = list()
        pop_action = getattr(list,"pop")
        goal_reached, visited, currentNode,number_of_states = self.traverse_states(frontier,pop_action)
        self.printResults(path=self._trace_path(currentNode,visited),goal_reached=goal_reached,algorithm="Depth First Search",time_elapsed=time.time() - start,number_of_states=number_of_states)
    
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

    def astar(self):
        class CubeState:
            state = None
            g = 0
            h = 0
            parent = None
            move = None
        bound  = util.patternDatabaseHeuristic(self.rubicsCube.cube)
        queue = util.PriorityQueue()
        currentNode = copy.deepcopy(self.rubicsCube)
        start = CubeState()
        start.state = currentNode
        start.h = bound
        visited = {self.rubicsCube.get_configuration_string(): (self.start_state_config,"-1")}
        queue.push(start,bound)
        while(not queue.isEmpty()):
            currentNode = queue.pop()
            if currentNode.state.is_cube_solved():
                goal_reached = True
                break
            else:
                for action,rotation in self.rotations:
                    new = CubeState()
                    new.state = copy.deepcopy(currentNode.state)
                    new.g = currentNode.g + 1
                    new.parent = currentNode
                    new.move = action
                    new.state.scramble([rotation])
                    new.h = util.patternDatabaseHeuristic(new.state.cube)
                    config_string = new.state.get_configuration_string()
                    if not config_string in visited:
                        visited[config_string] = (currentNode.state.get_configuration_string(), action)
                        queue.push(new,new.g+new.h)
                    if new.state.is_cube_solved():
                        print(new)
                        goal_reached = True
                        return goal_reached,visited,new.state,len(visited)-1
        return goal_reached,visited,currentNode,len(visited)-1 
            
    def astarsearch(self):
        util.load_cornerpatterns()
        util.load_edgepatterns()
        start = time.time()
        goal_reached, visited, currentNode,number_of_states = self.astar()
        self.printResults(path=self._trace_path(currentNode,visited),goal_reached=goal_reached,algorithm="A* Search",time_elapsed=time.time() - start,number_of_states=number_of_states)    

