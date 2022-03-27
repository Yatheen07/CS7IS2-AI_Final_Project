from msilib.schema import Error
import sqlite3
import time
import numpy as np
from model import scrambler
import util
from model.cube import RubicsCube,CubeSolver
from model.scrambler import Scrammbler
class Cube:
    cube = None
    cost = 0

cornermap = dict()
edgemap = dict()
rubicsCube = RubicsCube()
goal = rubicsCube.cube
cubeSolver = CubeSolver()
scramble = Scrammbler()

def generateCornerPatterns():
    start = time.time()
    print('Generating corner cubes patterns')
    queue = list()
    print('Goal string = ',util.getCornerString(goal))
    cornermap[util.getCornerString(goal)] = 0
    curr = Cube()
    curr.cost = 0
    curr.cube = np.array(goal)
    queue.append(curr)
    while(len(queue)!=0):
        curr = queue.pop(0)
        if(curr.cost < 6):
            childCost = curr.cost + 1
            for key,action in scramble.action_map.items():
                child = Cube()
                child.cube = np.array(curr.cube)
                child.cost = childCost
                action(cubeSolver,child.cube)
                string  = util.getCornerString(child.cube)
                if string not in cornermap.keys():
                    print(string)
                    cornermap[string] = child.cost
                    queue.append(child)
    print('Corner pattern generation complete')
    print('Total Patterns generated are ',len(cornermap))
    end = time.time()
    print(f'The time taken to generate pattern : {round(end - start, 2)}')

def generateEdgePattern():
    end = time.time()
    start = time.time()
    print('Generating edge cubes patterns')
    queue = list()
    print('Goal string = ',util.getEdgeString(goal))
    edgemap[util.getEdgeString(goal)] = 0
    curr = Cube()
    curr.cost = 0
    curr.cube = np.array(goal)
    queue.append(curr)
    while(len(queue)!=0):
        curr = queue.pop(0)
        if(curr.cost < 6):
            childCost = curr.cost + 1
            for key,action in scramble.action_map.items():
                child = Cube()
                child.cube = np.array(curr.cube)
                child.cost = childCost
                action(cubeSolver,child.cube)
                string  = util.getEdgeString(child.cube)
                if string not in edgemap.keys():
                    print(string)
                    edgemap[string] = child.cost
                    queue.append(child)
    print('Edge pattern generation complete')
    print('Total Patterns generated are ',len(edgemap))
    end = time.time()
    print(f'The time taken to generate pattern : {round(end - start, 2)}')


def main():
    try:
        con1 = sqlite3.connect('pattern.db')
        print("Creating corner pattern database");
        cursor1 = con1.execute('CREATE TABLE CORNER_PATTERN(CORNERS VARCHAR2(100),VALUE INT)')
        print('Corner pattern Table created sucessfully')
        con2 = sqlite3.connect('edgepattern.db')
        print("Creating edge pattern database");
        cursor2 = con2.execute('CREATE TABLE EDGE_PATTERN(EDGES VARCHAR2(100),VALUE INT)')
        print('Edge pattern Table created sucessfully')
        generateCornerPatterns()
        generateEdgePattern()
        cursor1.executemany('INSERT INTO CORNER_PATTERN(CORNERS, VALUE) VALUES (?, ?)', cornermap.items())
        con1.commit()
        cursor2.executemany('INSERT INTO EDGE_PATTERN(EDGES, VALUE) VALUES (?, ?)', edgemap.items())
        con2.commit()
    except Error as e:
        print(e,'Error Occurred')
    finally:
        cursor1.close()
        con1.close()
        cursor2.close()
        con2.close()

    
    
if __name__ == '__main__':
    main()