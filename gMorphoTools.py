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
    Gout = Gin.copy()
    for v in nx.nodes_iter(Gin):
        for vv in nx.all_neighbors(Gin, v):
            if Gin.node[v]['class'] < Gin.node[vv]['class']:
                Gout.node[v]['class'] = Gin.node[vv]['class']
    if stuffToDraw:
        dt.drawFromClasses(Gout, stuffToDraw[0], stuffToDraw[1])
    return Gout

def dilatation(G, order, stuffToDraw = None):
    '''
    Enables multiple dilatations in a row
    '''
    for k in range(1, order + 1):
        G = simpleDilation(G, stuffToDraw)
    return G

def simpleErosion(Gin, stuffToDraw = None):
    Gout = Gin.copy()
    for v in nx.nodes_iter(Gin):
        for vv in nx.all_neighbors(Gin, v):
            if Gin.node[v]['class'] > Gin.node[vv]['class']:
                Gout.node[v]['class'] = Gin.node[vv]['class']
    if stuffToDraw:
        dt.drawFromClasses(Gout, stuffToDraw[0], stuffToDraw[1])
    return Gout

def erosion(G, order, stuffToDraw = None):
    '''
    Enable multiple erosions in a row
    '''
    for k in range(1, order + 1):
        G = simpleErosion(G, stuffToDraw)
    return G

def closing(G, order, stuffToDraw = None):
    '''
    Using the fact that a closing in the composition of a dilatation by an erosion
    '''
    G = dilatation(G, order)
    G = erosion(G, order)
    if stuffToDraw:
        dt.drawFromClasses(G, stuffToDraw[0], stuffToDraw[1])
    return G

def opening(G, order, stuffToDraw = None):
    '''
    Using the fact that an opening is tha composition of an erosion by a dilatation
    '''
    G = erosion(G, order)
    G = dilatation(G, order)
    if stuffToDraw:
        dt.drawFromClasses(G, stuffToDraw[0], stuffToDraw[1])
    return G

def distGraph(Gin, fromNodeNumber, N):
    '''
    Based on Dijkstra algorithm. Assuming that 2 neighbor nodes have a distance = 1
    fromNodeNumber is a list!
    N is the size of the graph
    Returns a decimal graph (same graph but with attribute 'dist' in fact) from a binary graph
    '''
    Gout = Gin.copy()
    distGout = [float("inf") for N in range(0, N)]
    for v in fromNodeNumber:
        distGout[v] = 0
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

def skeletize(Gin, N, nodesToSkeletize, otherNodes = None):
    '''
    This will compute and return the skeleton of a binary graph Gin
    This is done by computing the distance function from our element to the background nodes and then by finding local extremum in distance graph. 
    If background nodes are given they are computed here.
    '''
    if not otherNodes:
        otherNodes = [n for n in range(0, N) if (n not in nodesToSkeletize)]
    
    GDist = distGraph(Gin, otherNodes, N)
    Gout = Gin.copy()
    
    #Find local extremum in GDist and only them in Gout
    for v in nx.nodes_iter(Gout):
        Gout.node[v]['class'] = 0
    for v in nodesToSkeletize:
        if ([True for x in nx.all_neighbors(GDist, v)] == [True for x in nx.all_neighbors(GDist, v) if (GDist.node[v]['dist'] >= GDist.node[x]['dist'])]):
            Gout.node[v]['class'] = 1
    
    return Gout


