import sqlite3
import time
import threading
import numpy as np
import copy
from model import scrambler
import util
from model.cube import RubicsCube
from model.scrambler import Scrammbler
import logging
logging.basicConfig(filename="patternstd.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
#Let us Create an object 
logger=logging.getLogger() 
class Cube:
    cube = None
    cost = 0

cornermap = dict()
edgemap = dict()
rubicsCube = RubicsCube(size=3)
goal = rubicsCube.cube
print(goal)
scramble = Scrammbler()

def generateCornerPatterns():
    try:
        con = sqlite3.connect('pattern.db')
        print("Creating corner pattern database");
        cursor = con.execute('CREATE TABLE CORNER_PATTERN(CORNERS VARCHAR2(100),VALUE INT)')
        print('Corner pattern Table created sucessfully')
        count = 0
        start = time.time()
        print('Generating corner cubes patterns')
        queue = list()
        print('Goal string = ',util.getCornerString(goal))
        cornermap[util.getCornerString(goal)] = 0
        curr = Cube()
        curr.cost = 0
        curr.cube = copy.deepcopy(rubicsCube)
        # curr.cube = np.array(goal)
        queue.append(curr)
        while(len(queue)!=0):
            curr = queue.pop(0)
            logger.debug('Current depth %s',str(curr.cost))
            logger.info('Current depth %s',str(curr.cost))
            if(curr.cost < 4):
                childCost = curr.cost + 1
                for key,action in scramble.action_map.items():
                    new_node = copy.deepcopy(curr.cube)
                    new_node.scramble([action])
                    child = Cube()
                    # child.cube = np.array(curr.cube)
                    child.cube = new_node
                    child.cost = childCost
                    string  = util.getCornerString(child.cube.cube)
                    if string not in cornermap.keys():
                        #print(string)
                        cornermap[string] = child.cost
                        queue.append(child)
                count += len(edgemap)
        print('Corner pattern generation complete')
        print('Total Patterns generated are ',len(cornermap))
        logger.debug('Corner pattern generation complete')
        logger.debug('Total pattern %s',str(len(cornermap)))
        end = time.time()
        print(f'The time taken to generate pattern : {round(end - start, 2)}')
        cursor.executemany('INSERT INTO CORNER_PATTERN(CORNERS, VALUE) VALUES (?, ?)', cornermap.items())
        con.commit()
        print('Insert complete')
        cornermap.clear()
    except Exception as e:
        print(e,'Error Occurred')
    finally:
        cursor.close()
        con.close()

def generateEdgePattern():
    try:
        con = sqlite3.connect('edgepattern.db')
        print("Creating edge pattern database");
        cursor = con.execute('CREATE TABLE EDGE_PATTERN(EDGES VARCHAR2(100),VALUE INT)')
        print('Edge pattern Table created sucessfully')
        start = time.time()
        count = 0
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
            if(curr.cost < 5):
                childCost = curr.cost + 1
                for key,action in scramble.action_map.items():
                    child = Cube()
                    child.cube = np.array(curr.cube)
                    child.cost = childCost
                    action(cubeSolver,child.cube)
                    string  = util.getEdgeString(child.cube)
                    if string not in edgemap.keys():
                        edgemap[string] = child.cost
                        queue.append(child)
                count += len(edgemap)
            else:
                break
        print('Edge pattern generation complete')
        print('Total Patterns generated are ',len(edgemap))
        end = time.time()
        print(f'The time taken to generate pattern : {round(end - start, 2)}')
        cursor.executemany('INSERT INTO EDGE_PATTERN(EDGES, VALUE) VALUES (?, ?)', edgemap.items())
        con.commit()
        print('Insert complete')
        edgemap.clear()
    except Exception as e:
        print(e,'Error Occurred')
    finally:
        cursor.close()
        con.close()

def main():
    try: 
        generateCornerPatterns()
        #generateEdgePattern()
        # cursor1.executemany('INSERT INTO CORNER_PATTERN(CORNERS, VALUE) VALUES (?, ?)', cornermap.items())
        # con1.commit()
        # cursor2.executemany('INSERT INTO EDGE_PATTERN(EDGES, VALUE) VALUES (?, ?)', edgemap.items())
        # con2.commit()
    except Exception as e:
        print(e,'Error Occurred')
    
if __name__ == '__main__':
    main()