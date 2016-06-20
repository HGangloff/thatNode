import numpy as np
import networkx as nx
import tools.drawTools as dt
import tools.gMorphoTools as gmt

N = 100

#Graph with no edges
G = nx.empty_graph(N)

pos = nx.random_layout(G)
nx.set_node_attributes(G, 'pos', pos)
#We will draw the edges according to k nearest neightbors algorithms
G = gmt.delaunay(G)
G, foreground, background = gmt.connectedComponents(G, N, 2, 5)

#Lets test the reconstruction
Gmark = G.copy()
for v in nx.nodes_iter(Gmark):
    Gmark.node[v]['class'] = 0
Gmark.node[foreground[0]]['class'] = 1 #We take one marker
dt.drawFromClasses(G, pos)
dt.drawFromClasses(Gmark, pos)
G2 = gmt.reconstruct(G, Gmark, N)
dt.drawFromClasses(G2, pos)
