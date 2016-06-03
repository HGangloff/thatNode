import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def drawVoronoi(G, classes, pos):
    points = np.zeros((nx.number_of_nodes(G), 2))
    for k, v in pos.items():
        points[k, :] = v
    vor = Voronoi(points)
    regions2 = vor.regions
    point_region2 = vor.point_region
    #Treating the empty list problem, if voronoi returns that empty list: Do the needed treatements. Else an exception will be raised by index and it needs to be handled but it would mean that there is no empty list, so nothing to worry about
    try:
        idx = regions2.index([])
    except ValueError as v:
        pass
    else:
        regions2 = [r for r in regions2 if r != []]
        for i, x in enumerate(point_region2):
            if x >= idx:
                point_region2[i] -= 1

    voronoi_plot_2d(vor, show_vertices = False, show_points = False)

    for idx, region in enumerate(regions2):
        if (not -1 in region):
            polygon = [vor.vertices[i] for i in region]
            if G.node[point_region2[idx]]['class'] == 0:
                plt.fill(*zip(*polygon), 'k')
            else:
                plt.fill(*zip(*polygon), 'w')
    #nx.draw_networkx(G, pos)
    plt.show()

def drawFromClasses(G, pos, classes): 
    classes = nx.get_node_attributes(G, 'class')
    black_nodes = [k for k, v in classes.items() if v == 0]
    white_nodes = [k for k, v in classes.items() if v == 1]
    nx.draw_networkx(G, pos, with_labels = False)
    nx.draw_networkx_nodes(G, pos, black_nodes, node_color = '0.2', linewidths = 0)
    nx.draw_networkx_nodes(G, pos, white_nodes, node_color = 'w', linewidths = 0)
    nx.draw_networkx_edges(G, pos, edge_color = 'k')
    plt.show()
