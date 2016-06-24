import networkx as nx
import numpy as np
import tools.binaryOperators as bo
from scipy.spatial import Delaunay
from collections import deque
###########
#Exception#
###########
class BreakTwoLoops( Exception ):
    pass

#########################
#Graph creation function#
#########################
def noEdgeGraph(numberOfNodes):
    '''
    Returns an empty graph ie, with no edges, with the required number of nodes
    '''
    return nx.empty_graph(numberOfNodes)

################################
#Graph position setup functions#
################################
def random_pos(G):
    '''
    Set random positions for G nodes according to networkx algorithm 
    AND add position to 'pos' property of nodes
    '''
    pos = nx.random_layout(G)
    nx.set_node_attributes(G, 'pos', pos)

###########################
#Edges creations functions#
###########################
def knn(G, k):
    '''
    Create edges to G according to the k nearest neighbours algorith
    This is dependent on distance between nodes, so dependent on the 'pos' attribute
    '''
    for v in nx.nodes_iter(G):
        for vv in nx.nodes_iter(G):
            if v != vv and (G.node[vv]['pos'][0] - G.node[v]['pos'][0])**2 + (G.node[vv]['pos'][1] - G.node[v]['pos'][1])**2 < k**2:
                G.add_edge(v, vv)

def delaunay(G):
    '''
    Creates and return the graph with edges corresponding to the Delaunay Triangulation of the graph
    G is the graph without nodes, with the position of the nodes as 'pos' attribute

    Returns G with new edges correspondig to Delaunay triangulation
    (this implementation costs a lot)
    '''
    #scipy function needs a list of coordinates tocompute Delaunay:
    points = [[G.node[v]['pos'][0], G.node[v]['pos'][1]] for v in nx.nodes_iter(G)]
    points = np.array(points)
    tri = Delaunay(points)
    for i in points[tri.simplices]:
        for j in range(0, 3):
            k = (j + 1) % 3 
            for v in nx.nodes_iter(G):
                for vv in nx.nodes_iter(G):
                    if (G.node[v]['pos'][0] == i[j][0]) and (G.node[v]['pos'][1] == i[j][1]) and (G.node[vv]['pos'][0] == i[k][0]) and (G.node[vv]['pos'][1] == i[k][1]):
                        G.add_edge(v, vv)

#################################
#Binary class creation functions#
#################################
def oneOfTwo(G):
    '''
    Create a binary graph with 50% nodes in one class and 50% nodes in another
    G is the graph
    N is the size of the graph
    
    Returns 2 lists with the nodes numbers belonging to each class
    '''
    N = nx.number_of_nodes(G)
    classes = {i:j for i in range(0, N) for j in range(0, 2) if i % 2 == j}
    nx.set_node_attributes(G, 'class', classes)
    foreground = [k for k,v in classes.items() if v == 1]
    background = [k for k,v in classes.items() if v == 0]
    return (foreground, background)

def oneVAll(G, thatNode = None):
    '''
    Create a binary graph : only one node is in the 'opposite' class
    G is the graph
    N the size of the graph
    thatNode allows the user to choose which node is the lonely one
    Returns the graph with a new attribute class.
    Also returns 2 lists with the nodes numbers belonging to each class
    '''
    N = nx.number_of_nodes(G)
    if not thatNode:
        thatNode = N // 2
    classes = {}
    for i in range(0, N):
        if i == thatNode:
            classes[i] = 1
        else:
            classes[i] = 0
    nx.set_node_attributes(G, 'class', classes)
    foreground = [k for k,v in classes.items() if v == 1]
    background = [k for k,v in classes.items() if v == 0]
    return (foreground, background)

def connectedComponents(G, number, size):
    '''
    Create some connected components in a binary graph.
    G is the graph
    N is the size of the graph
    number is the nb of connected component to create
    size is the size of the connected component

    Returns the graph with a new attribute class.
    Also returns 2 lists with the nodes numbers belonging to each class

    Each different connected component are created with different class value
    But then all class values != 0 are set to 1 (binary graph)
    '''
    N = nx.number_of_nodes(G)
    classes = {N:0 for N in range(0, N)}
    nx.set_node_attributes(G, 'class', classes)
    n = 1
    while n <= number:
        G.node[n * (N // number) - 1]['class'] = n
        i = 1
        while i < size:
            try:
                for v in nx.nodes_iter(G):
                    if G.node[v]['class'] == n:
                        for vv in nx.all_neighbors(G, v):
                            if G.node[vv]['class'] not in range(1, n + 1):
                                G.node[vv]['class'] = n
                                i += 1
                                if i == size:
                                    raise BreakTwoLoops
            except BreakTwoLoops:
                pass

        n += 1
    
    #Because we make a binary graph :
    for v in nx.nodes_iter(G): 
        if G.node[v]['class'] > 0:
            G.node[v]['class'] = 1
    foreground = [k for k,v in nx.get_node_attributes(G, 'class').items() if v == 1]
    background = [k for k,v in nx.get_node_attributes(G, 'class').items() if v == 0]
    return (foreground, background)

    

################################
#Morphological operations tools#
################################

def simpleDilation(Gin):
    '''
    Performs a simple dilatation. If draw is True, it will directly display the result
    '''

    Gout = Gin.copy()
    for v in nx.nodes_iter(Gin):
        for vv in nx.all_neighbors(Gin, v):
            if Gin.node[v]['class'] < Gin.node[vv]['class']:
                Gout.node[v]['class'] = Gin.node[vv]['class']
    return Gout

def dilatation(G, order):
    '''
    Enables multiple dilatations in a row. 
    If draw is given, it will directly display the result
    '''

    for k in range(1, order + 1):
        G = simpleDilation(G)
    return G

def simpleErosion(Gin):
    '''
    Performs a simple erosion
    If draw is given, it will directly display the result
    '''

    Gout = Gin.copy()
    for v in nx.nodes_iter(Gin):
        for vv in nx.all_neighbors(Gin, v):
            if Gin.node[v]['class'] > Gin.node[vv]['class']:
                Gout.node[v]['class'] = Gin.node[vv]['class']
    return Gout

def erosion(G, order):
    '''
    Enable multiple erosions in a row
    If draw is given, it will directly display the result
    '''

    for k in range(1, order + 1):
        G = simpleErosion(G)
    return G

def closing(G, order):
    '''
    Using the fact that a closing in the composition of a dilatation by an erosion
    '''
    G = dilatation(G, order)
    G = erosion(G, order)
    return G

def opening(G, order):
    '''
    Using the fact that an opening is tha composition of an erosion by a dilatation
    '''
    G = erosion(G, order)
    G = dilatation(G, order)
    return G

def distGraph(Gin, fromNodeNumber):
    '''
    Based on Dijkstra algorithm. Assuming that 2 neighbor nodes have a distance = 1
    fromNodeNumber is a list!
    N is the size of the graph
    Returns a decimal graph (same graph but with attribute 'dist' in fact) from a binary graph
    ''' 
    N = nx.number_of_nodes(Gin)
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

def skeletizeRaw(Gin, nodesToSkeletize, otherNodes = None):
    '''
    This will compute and return the skeleton of a binary graph Gin
    This is done by computing the distance function from our element to the background nodes and then by finding local extremum in distance graph. 
    If background nodes are given they are computed here.
    '''
    N = nx.number_of_nodes(Gin)
    if not otherNodes:
        otherNodes = [n for n in range(0, N) if (n not in nodesToSkeletize)]
    
    GDist = distGraph(Gin, otherNodes)
    Gout = Gin.copy()
    
    #Find local extremum in GDist and only them in Gout
    for v in nx.nodes_iter(Gout):
        Gout.node[v]['class'] = 0
    for v in nodesToSkeletize:
        if ([True for x in nx.all_neighbors(GDist, v)] == [True for x in nx.all_neighbors(GDist, v) if (GDist.node[v]['dist'] >= GDist.node[x]['dist'])]):
            Gout.node[v]['class'] = 1
    
    return Gout

def reconstruct(G, Gmark):
    '''
    Compute the reconstruction of graph G with markers from graph Gmark
    G is the original graph
    Gmark is the graph with markers (same structure as G)
    '''
    N = nx.number_of_nodes(G)
    Gout = G.copy()
    for v in nx.nodes_iter(Gout):
        Gout.node[v]['class'] = 0
    
    q = deque()
    seen = {n:False for n in range(0, N)}
    nx.set_node_attributes(Gmark, 'seen', seen)
    
    for v in nx.nodes_iter(Gmark):
        if Gmark.node[v]['class'] == 1:
            q.appendleft(v)
    while q:
        v = q.pop()
        if G.node[v]['class'] == 1:
            Gout.node[v]['class'] = 1
            Gmark.node[v]['seen'] = True
            for vv in nx.all_neighbors(G, v): 
                if not Gmark.node[vv]['seen']:
                    q.appendleft(vv)
    return Gout

def label(G):
    '''
    Given a binary graph G, it will create a decimal graph with another 'class' (label) for each connected component
    This algorithm uses the principle of reconstruction
    '''
    N = nx.number_of_nodes(G)
    
    Gout = G.copy() #Thus, all that should be of class 0 in Gout is already ok
    
    q = deque()
    seen = {n:False for n in range(0, N)}
    nx.set_node_attributes(G, 'seen', seen)
    lbl = 0

    for v in nx.nodes_iter(G):
        if G.node[v]['class'] == 0:
            G.node[v]['seen'] = True
        elif G.node[v]['seen'] == False:
            lbl += 1
            G.node[v]['seen'] = True
            q.appendleft(v)
            while q:
                vv = q.pop()
                if G.node[vv]['class'] == 1:
                    Gout.node[vv]['class'] = lbl
                    G.node[vv]['seen'] = True
                    for vvv in nx.all_neighbors(G, vv):
                        if not G.node[vvv]['seen']:
                            q.appendleft(vvv)
    print("Labelling result : Number of connected components : " + str(lbl))
    return Gout


def externalGradient(G):
    return bo.binarySub(simpleDilation(G), G)

def internalGradient(G):
    return bo.binarySub(G, simpleErosion(G))

def symetricalGradient(G):
    return bo.binarySub(simpleDilation(G), simpleErosion(G))

def laplacian(G):
    return bo.binarySub(externalGradient(G), internalGradient(G))

def zonesOfInfluence(G):
    '''
    Given a binary graph G, compute the zones of influence of eachof its connected components
    -We note each connected component by labelling
    -We compute distgraph for all connected components
    -For all nodes not in a connected component we seek for the min distance
    -If a node is at equal distance from 2 connected components, the node belongs to none
    '''
    Glbl = label(G)
    Gzi = Glbl.copy()
    lblDict = nx.get_node_attributes(Glbl, 'class')
    lblRange = lblDict[max(lblDict, key = lambda x: lblDict.get(x))]
    distGraphList = []
    for i in range(lblRange):
        thatNodes = [v for v in nx.nodes_iter(Glbl) if Glbl.node[v]['class'] == (i + 1)]
        distGraphList.append(distGraph(Glbl, thatNodes))
    for v in nx.nodes_iter(Glbl):
        if Glbl.node[v]['class'] == 0:
            distances = []
            minIsTwiceOrMore = False
            for i in range(lblRange):
                distances.append(distGraphList[i].node[v]['dist'])
            
            #Check if element at equal min dist
            m = min(distances) #returns the value
            mm = distances.index(m)
            distances.remove(m)
            if m in distances: #if it is still in the list...
                minIsTwiceOrMore = True

            if not minIsTwiceOrMore: #if element appears twice or more ie node at equal distance from 2 conn comp
                Gzi.node[v]['class'] = -(mm + 1)
    return Gzi

