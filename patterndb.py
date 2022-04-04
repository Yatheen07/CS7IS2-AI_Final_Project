import sqlite3
import time
import threading
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
        curr.cube = np.array(goal)
        queue.append(curr)
        while(len(queue)!=0):
            curr = queue.pop(0)
            if(curr.cost < 8):
                childCost = curr.cost + 1
                for key,action in scramble.action_map.items():
                    child = Cube()
                    child.cube = np.array(curr.cube)
                    child.cost = childCost
                    action(cubeSolver,child.cube)
                    string  = util.getCornerString(child.cube)
                    if string not in cornermap.keys():
                        #print(string)
                        cornermap[string] = child.cost
                        queue.append(child)
                count += len(edgemap)
                print('Inserting into corner pattern database')        
                cursor.executemany('INSERT INTO CORNER_PATTERN(CORNERS, VALUE) VALUES (?, ?)', cornermap.items())
                con.commit()
                cornermap.clear()
        print('Corner pattern generation complete')
        print('Total Patterns generated are ',len(cornermap))
        end = time.time()
        print(f'The time taken to generate pattern : {round(end - start, 2)}')
    except Exception as e:
        print(e,'Error Occurred')
    finally:
        cursor.close()
        con.close()

def generateEdgePattern(con,cursor):
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
            if(curr.cost <= 6):
                childCost = curr.cost + 1
                for key,action in scramble.action_map.items():
                    child = Cube()
                    child.cube = np.array(curr.cube)
                    child.cost = childCost
                    action(cubeSolver,child.cube)
                    string  = util.getEdgeString(child.cube)
                    if string not in edgemap.keys():
                        #print(string)
                        edgemap[string] = child.cost
                        queue.append(child)
                count += len(edgemap)
                print('Inserting into edge pattern database')
                cursor.executemany('INSERT INTO EDGE_PATTERN(EDGES, VALUE) VALUES (?, ?)', edgemap.items())
                con.commit()
                edgemap.clear()
            else:
                break
        print('Edge pattern generation complete')
        print('Total Patterns generated are ',count)
        end = time.time()
        print(f'The time taken to generate pattern : {round(end - start, 2)}')
    except Error as e:
        print(e,'Error Occurred')
    finally:
        cursor.close()
        con.close()

def main():
    try: 
        a = threading.Thread(target = generateCornerPatterns)
        b = threading.Thread(target = generateEdgePattern)
        a.start()
        b.start()
        # generateCornerPatterns(con1,cursor1)
        # generateEdgePattern(con2,cursor2)
        # cursor1.executemany('INSERT INTO CORNER_PATTERN(CORNERS, VALUE) VALUES (?, ?)', cornermap.items())
        # con1.commit()
        # cursor2.executemany('INSERT INTO EDGE_PATTERN(EDGES, VALUE) VALUES (?, ?)', edgemap.items())
        # con2.commit()
    except Error as e:
        print(e,'Error Occurred')
    
if __name__ == '__main__':
    main()