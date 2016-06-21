import tools.drawTools as dt
import tools.gMorphoTools as gmt

#Graph creation part
N = 100
G = gmt.noEdgeGraph(N)
gmt.random_pos(G)
gmt.delaunay(G)


foreground, background = gmt.connectedComponents(G, 5, 2)
dt.drawFromClasses(G)

Glbl = gmt.label(G)

'''
#Test the reconstruction
Gmark = G.copy()
for v in nx.nodes_iter(Gmark):
    Gmark.node[v]['class'] = 0
Gmark.node[foreground[0]]['class'] = 1 #We take one marker
dt.drawFromClasses(G)
dt.drawFromClasses(Gmark)
G2 = gmt.reconstruct(G, Gmark)
dt.drawFromClasses(G2)
'''
