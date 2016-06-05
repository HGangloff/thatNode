import networkx as nx
import numpy as np
import drawTools as dt
import networkx as nx
import time
from collections import deque

###########################
#Edges creations functions#
###########################
def knn(G, k):
    for v in nx.nodes_iter(G):
        for vv in nx.nodes_iter(G):
            if v != vv and (G.node[vv]['pos'][0] - G.node[v]['pos'][0])**2 + (G.node[vv]['pos'][1] - G.node[v]['pos'][1])**2 < k**2:
                G.add_edge(v, vv)
    return G
#################################
#Binary class creation functions#
#################################

#Equal class distribution
def oneOfTwo(N):
    classes = {i:j for i in range(0, N) for j in range(0, 2) if i % 2 == j}
    return classes
#One node vs all :
def oneVAll(N, thatNode = None):
    if not thatNode:
        thatNode = N // 2
    classes = {}
    for i in range(0, N):
        if i == thatNode:
            classes[i] = 1
        else:
            classes[i] = 0
    return classes
#Small group (this requires a graph with edges)
def small(G, N, n):
    classes = {N:0 for N in range(0, N)}
    classes[N // 2] = 1
    i = 1
    while i < n:
        for v in nx.nodes_iter(G):
            if classes[v] == 1:
                for vv in nx.all_neighbors(G, v):
                    if (i < n) and (classes[vv] != 1):
                        classes[vv] = 1
                        i += 1
    return classes

    

################################
#Morphological operations tools#
################################

def simpleDilation(Gin, stuffToDraw = None):
    #Careful with the copy:
    Gout = Gin.copy()
    for v in nx.nodes_iter(Gin):
        for vv in nx.all_neighbors(Gin, v):
            if Gin.node[v]['class'] < Gin.node[vv]['class']:
                Gout.node[v]['class'] = Gin.node[vv]['class']
    if stuffToDraw:
        dt.drawFromClasses(Gout, stuffToDraw[0], stuffToDraw[1])
    return Gout

def dilatation(Gin, order, stuffToDraw = None):
    for k in range(1, order + 1):
        Gin = simpleDilation(Gin, stuffToDraw)
    return Gin

def simpleErosion(Gin, stuffToDraw = None):
    Gout = Gin.copy()
    for v in nx.nodes_iter(Gin):
        for vv in nx.all_neighbors(Gin, v):
            if Gin.node[v]['class'] > Gin.node[vv]['class']:
                Gout.node[v]['class'] = Gin.node[vv]['class']
    if stuffToDraw:
        dt.drawFromClasses(Gout, stuffToDraw[0], stuffToDraw[1])
    return Gout

def erosion(Gin, order, stuffToDraw = None):
    for k in range(1, order + 1):
        Gin = simpleErosion(Gin, stuffToDraw)
    return Gin

def closing(Gin, order, stuffToDraw = None):
    Gin = dilatation(Gin, order)
    Gin = erosion(Gin, order)
    if stuffToDraw:
        dt.drawFromClasses(Gin, stuffToDraw[0], stuffToDraw[1])
    return Gin

def opening(Gin, order, stuffToDraw = None):
    Gin = erosion(Gin, order)
    Gin = dilatation(Gin, order)
    if stuffToDraw:
        dt.drawFromClasses(Gin, stuffToDraw[0], stuffToDraw[1])
    return Gin

def computeDistGraph(Gin, fromNodeNumber, N):
    '''
    Based on Dijkstra algorithm. Assuming that 2 neighbor nodes have a distance = 1
    Returns a decimal graph from a binary graph
    '''
    Gout = Gin.copy()
    distGout = [float("inf") for N in range(0, N)]
    distGout[fromNodeNumber] = 0
    thatNodeList = {v:distGout[v] for v in nx.nodes_iter(Gin)}
    while thatNodeList:
        u = min(thatNodeList, key = thatNodeList.get)
        thatNodeList.pop(u, None)
        for v in nx.all_neighbors(Gin, u):
            alt = distGout[u] + 1 #change this line to extend to weighted and other graphs
            if alt < distGout[v]:
                distGout[v] = alt
                thatNodeList[v] = alt
    
    distGout = {n:distGout[n] for n in range(0, N)}
    nx.set_node_attributes(Gout, 'dist', distGout)
    return Gout
