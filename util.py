import numpy as np
xInitial = np.array([
        ['R' ,'G' ,'G'],
        ['G','W','W'],
        ['Y','Y','B'],
        ['G', 'E', 'G'],
        ['G', 'G', 'G'],
        ['G', 'E', 'G'],
        ['R', 'E', 'R'],
        ['R', 'R', 'R'],
        ['R', 'E', 'R'],
        ['B', 'E', 'B'],
        ['B', 'B', 'B'],
        ['B', 'E', 'B'],
        ['O', 'E', 'O'],
        ['O', 'O', 'O'],
        ['O', 'E', 'O'],
        ['Y', 'E', 'Y'],
        ['Y', 'Y', 'Y'],
        ['Y', 'E', 'Y']
    ])

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
            edges = edges + xInitial[i,1]
        else:
            edges = edges + xInitial[i,0] + xInitial[i,2]
    return edges
