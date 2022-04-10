import numpy as np
import heapq
import sqlite3

cornerdb = dict()
edgedb = dict()

class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

def getCornerString(x):
    cornerString = ''
    for i in range(18):
        if i%3==0 or i%3==2:
            cornerString = cornerString + x[i,0] + x[i,2]
    return cornerString


def getEdgeString(x):
    edges = ''
    for i in range(18):
        if i%3==0 or i%3==2:
            edges = edges + x[i,1]
        else:
            edges = edges + x[i,0] + x[i,2]
    return edges

def load_cornerpatterns():
    conn = sqlite3.connect('pattern.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM CORNER_PATTERN")
    rows = cur.fetchall()
    for x, y in rows:
        cornerdb[x] = y

def load_edgepatterns():
    conn = sqlite3.connect('edgepattern.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM EDGE_PATTERN")
    rows = cur.fetchall()
    for x, y in rows:
        edgedb[x] = y

def patternDatabaseHeuristic(cube):
    cornerstring = getCornerString(cube)
    edgestring = getEdgeString(cube)
    cornerh = cornerdb.get(cornerstring,-1)
    edgeh = edgedb.get(edgestring,-1)
    if cornerh != -1 and edgeh !=-1:
        return max(cornerh,edgeh)
    elif cornerh == -1 and edgeh == -1:
        return 0
    elif cornerh == -1:
        return edgeh
    else:
        return cornerh

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


