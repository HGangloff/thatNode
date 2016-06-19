import numpy as np
import networkx as nx
import tools.drawTools as dt
import tools.gMorphoTools as gmt

N = 100

#Graph with no edges
G = nx.empty_graph(N)
#G = nx.scale_free_graph(N,alpha = 0.4, beta = 0.55, gamma = 0.05)
#G = G.to_undirected()
#Need to set a fixed position for all drawings
#pos = nx.spring_layout(G)

pos = nx.random_layout(G)
nx.set_node_attributes(G, 'pos', pos)
#We will draw the edges according to k nearest neightbors algorithms
G = gmt.delaunay(G)
G, foreground, background = gmt.connectedComponents(G, N, 2, 5)
dt.drawFromClasses(G, pos)
