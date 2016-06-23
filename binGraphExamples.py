#Imports from thatNode package
import tools.drawTools as dt
import tools.gMorphoTools as gmt

import networkx as nx

############################
#Binary graph creation part#
############################
N = 100 #Number of nodes
G = gmt.noEdgeGraph(N)
gmt.random_pos(G)
gmt.delaunay(G) #create edges using delaunay triangulation
foreground, background = gmt.connectedComponents(G, 1, 30) #create one connected component of 30 nodes (stored in foreground list)
dt.drawFromClasses(G, "G = Base binary graph") #draw the graph

################################
#Binary operators demonstration#
################################
#Perform an erosion of order 1
erodedG = gmt.simpleErosion(G)
dt.drawFromClasses(erodedG, "Erosion of G (order = 1)")

#Perform a dilatation of order 1
dilatedG = gmt.simpleDilation(G)
dt.drawFromClasses(dilatedG, "Dilatation of G (order = 1)")

#Perform an opening of order 1
openedG = gmt.opening(G, 1)
dt.drawFromClasses(openedG, "Opening of G (order = 1)")

#Perform a closing of order 1
closedG = gmt.closing(G, 1)
dt.drawFromClasses(closedG, "Closing of G (order = 1)")

#Perform a skeletization of 'foreground' nodes component
skG = gmt.skeletizeRaw(G, foreground)
dt.drawFromClasses(skG, "Skeleton of G")

#Get the distance graph from the nodes in 'foreground' list
distG = gmt.distGraph(G, foreground)
dt.drawDistanceGraph(distG, "Distance Graph (from the golden nodes component)")

#Perform a Laplacian transform
lapG = gmt.laplacian(G)
dt.drawFromClasses(lapG, "Laplacian of G")

#Perform a symetrical gradient
symG = gmt.symetricalGradient(G)
dt.drawFromClasses(symG, "Symetrical gradient of G")

#Perform an external gradient
extG = gmt.externalGradient(G)
dt.drawFromClasses(extG, "External gradient of G")

#Perform an internal gradient
intG = gmt.internalGradient(G)
dt.drawFromClasses(intG, "Internal gradient of G")

#Perform a geodesic reconstruction
foreground, background = gmt.connectedComponents(G, 2, 4)
dt.drawFromClasses(G, "G2 = Another base binary graph")
Gmark = G.copy() #Make a marker graph
for v in nx.nodes_iter(Gmark):
    Gmark.node[v]['class'] = 0
Gmark.node[foreground[0]]['class'] = 1 #We take one marker
reconsG = gmt.reconstruct(G, Gmark)
dt.drawFromClasses(Gmark, "Gmark = a marker on G2")
dt.drawFromClasses(reconsG, "Reconstruction of G2 by Gmark")

#Label the connected components
Glbl = gmt.label(G)
dt.drawLabelledGraph(Glbl, "Connected components labelling of G2")

#Compute the zones of influences of our connected components
Gzi = gmt.zonesOfInfluence(G)
dt.drawZoneofIGraph(Gzi, "Zones of influence of G2 connected components")
