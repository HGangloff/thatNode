import numpy as np
import networkx as nx
import drawTools as dt
import gMorphoTools as gmt

N = 300

#Graph with no edges
G = nx.empty_graph(N)

#Need to set a fixed position for all drawings
pos = nx.random_layout(G)
nx.set_node_attributes(G, 'pos', pos)

#We will draw the edges according to k nearest neightbors algorithms
G = gmt.knn(G, 0.1)

classes = gmt.small(G, N, 10)
nx.set_node_attributes(G, 'class', classes)

dt.drawFromClasses(G, pos, classes)

#G = gmt.dilatation(G, 3, [pos, classes])
#G = gmt.erosion(G, 3, [pos, classes])
G = gmt.closing(G, 5, [pos, classes])
