import numpy as np
import networkx as nx
import tools.drawTools as dt
import tools.gMorphoTools as gmt

N = 1000

#Graph with no edges
#G = nx.empty_graph(N)
G = nx.scale_free_graph(N,alpha = 0.9, beta = 0.05, gamma = 0.05)
G = G.to_undirected()
#Need to set a fixed position for all drawings
pos = nx.spring_layout(G)
nx.set_node_attributes(G, 'pos', pos)

#We will draw the edges according to k nearest neightbors algorithms
#G = gmt.knn(G, 0.1)

#/!\ put a number that can match with N :
classes = gmt.small(G, N, 10)
nx.set_node_attributes(G, 'class', classes)
foreground = [k for k,v in classes.items() if v == 1]
background = [k for k,v in classes.items() if v == 0]

dt.drawFromClasses(G, pos)

G = gmt.dilatation(G, 4, pos)
#GSkeletized = gmt.skeletizeRaw(G, N, foreground, background)
#dt.drawFromClasses(GSkeletized, pos)
