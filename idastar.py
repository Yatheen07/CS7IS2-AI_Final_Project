from itertools import count
import util
import sqlite3
import time
import math
import numpy as np
from model import scrambler
from util import PriorityQueue
from model.cube import RubicsCube,CubeSolver
from model.scrambler import Scrammbler
from model.scramble_configurations import scramble_configurations
import sys
import logging
logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
#Let us Create an object 
logger=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 
rr = RubicsCube()
scramble = Scrammbler()
cubeSolver = CubeSolver()
class State:
    cube = None
    g = 0
    h = 0
    parent = None
    move = None

def goal_reached(cube):
    for ref in [0, 3, 6, 9, 12, 15]:
        first = cube[ref, 0]
        for i in range(3):
            for j in range(3):
                if first != cube[ref + i, j]:
                    return False
    print('Gaol Reached')
    logger.debug('Gaol Reached')
    logger.info('Gaol Reached')
    flag = np.array_equal(rr.solved_config,cube)
    if flag:
        return flag
    return True
# checks if child ascendant of parent
def contains1(child, parent):
    curr = parent.parent
    while curr is not None:
        if np.array_equal(curr.cube, child): return True
        curr = curr.parent
    return False


# checks if frontier contains child
def contains2(child, frontier):
    for (n,p,i) in frontier.heap:
        if np.array_equal(i.cube, child): return True
    return False

def ida(cube):
    visited = set()
    state = State()
    state.cube = np.array(cube)
    state.h = util.patternDatabaseHeuristic(state.cube)
    queue = PriorityQueue()
    cost_limit = state.h
    nodes = 0
    branching_factors = list()
    frontier = list()
    while True:
        visited.add(state)
        print('New Level')
        logger.debug('New Level')
        logger.info('New Level')
        queue = PriorityQueue()
        minimum = math.inf
        # frontier.append(state)
        queue.push(state,state.g+state.h)
        # while len(frontier) != 0:
        while not queue.isEmpty():
            cubestate = queue.pop()
            #cubestate = frontier.pop()
            #print(cubestate.h+cubestate.g)
            if goal_reached(cubestate.cube):
                print('Goal Height:', cubestate.g)
                print('Branching Factor:', sum(branching_factors)/len(branching_factors))
                logger.debug('New Level')
                logger.info('New Level')
                # while curr is not None:
                #    if curr.move is not None:
                #        print(curr.move)
                #    curr = curr.parent
                print("Nodes Generated:", nodes)
                return
            if cubestate.g+cubestate.h > cost_limit:
                if minimum is None or new.g + new.h < minimum:
                        minimum = new.g + new.h
                continue
            else:
                for key,action in scramble.action_map.items():
                    nodes += 1
                    new = State()
                    new.cube = np.array(cubestate.cube)
                    new.g = cubestate.g + 1
                    new.parent = cubestate
                    action(cubeSolver,new.cube)
                    new.h = util.patternDatabaseHeuristic(new.cube)
                    if cubestate.parent is not None and (contains1(new.cube, cubestate) and contains2(new.cube,queue)):
                        continue
                    queue.push(new,new.g + new.h)
                    #frontier.append(new)
                    #b = b + 1
        cost_limit = minimum
        print('Limit Reched', str(cost_limit))
        logger.debug('Limit Reched %s',str(cost_limit))
        logger.info('Limit Reched %s',str(cost_limit))

def IDAStar(cubestate):
        dist = util.patternDatabaseHeuristic(cubestate)
        var = dist
        state = State()
        state.cube = np.array(cubestate)
        state.h = util.patternDatabaseHeuristic(state.cube)
        while True:
            visited = set()
            queue = util.PriorityQueue()
            queue.push(state,state.g+state.h)
            print("Threshold: ",var)
            var = IDAStarUtil(queue, var)
            # var = self.IDAStarUtil(queue, end, var)
            if ( isinstance(var, bool) ):
                return True
            elif( isinstance(var, int) ):
                if ( var == -1 ):
                    return False
        
def IDAStarUtil(q, cost_limit):
    # def IDAStarUtil(self, q, end, MaxDistance):   
        Count = 0
        CurrentDistance = -1
        while ( not q.isEmpty() ):
            Count += 1
            current_Node = q.pop()
            if (goal_reached(current_Node.cube)):
                print("No of Nodes visited: ", Count)
                print("Depth: ",current_Node.g)
                return True
            f  = current_Node.g+current_Node.h
            if (f > cost_limit ):
                if ( CurrentDistance != -1 and f < CurrentDistance ):
                    CurrentDistance = f
                elif ( CurrentDistance == -1 ):
                    CurrentDistance = f
                continue
             
            for key,action in scramble.action_map.items():
                new = State()
                new.cube = np.array(current_Node.cube)
                new.g = current_Node.g + 1
                new.parent = current_Node
                action(cubeSolver,new.cube)
                new.h = util.patternDatabaseHeuristic(new.cube)
                if current_Node.parent is not None and (contains1(new.cube, current_Node) and contains2(new.cube,q)):
                        continue
                q.push(new, new.g + new.h)
        print(Count)
        return CurrentDistance

def main():
    rubicsCube = RubicsCube()
    scrammbler = Scrammbler()
    scramble_sequence,unscramble_sequence = scrammbler.scramble(scramble_configurations[0])

#Scramble a fresh cube to get a initial state
    util.load_cornerpatterns()
    util.load_edgepatterns()
    rubicsCube.scramble(action_sequence=scramble_sequence)
    ida(rubicsCube.cube)
    #IDAStar(rubicsCube.cube)




if __name__ == "__main__":
    main()
