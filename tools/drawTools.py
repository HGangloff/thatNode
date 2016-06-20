import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def drawVoronoi(G, classes, pos):
    '''
    Should draw the Voronoi diagram of G. 
    NOT USABLE
    '''
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

def drawFromClasses(G): 
    '''
    Draws a binary graph with 2 different class in the 'class' attributes 
    '''
    pos = nx.get_node_attributes(G, 'pos')
    classes = nx.get_node_attributes(G, 'class')
    black_nodes = [k for k, v in classes.items() if v == 0]
    white_nodes = [k for k, v in classes.items() if v == 1]
    nx.draw_networkx(G, pos, with_labels = False)
    nx.draw_networkx_nodes(G, pos, black_nodes, node_color = '0.2', linewidths = 0)
    nx.draw_networkx_nodes(G, pos, white_nodes, node_color = 'y', linewidths = 0)
    nx.draw_networkx_edges(G, pos, edge_color = 'k')
    plt.show()

def drawDistanceGraph(G):
    '''
    Given a decimal graph (with attribute 'dist') it draws the distance graph using nodes with dist = 0 as basis
    '''
    pos = nx.get_node_attributes(G, 'pos')
    dist = nx.get_node_attributes(G, 'dist')
    distRange = [v for k, v in dist.items() if v != float("inf")]
    distRange = list(set(distRange)) #kill duplicates
    nx.draw_networkx(G, pos, with_labels = False)
    #Draw the ones at inf distance :
    thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['dist'] == float("inf")]
    nx.draw_networkx_nodes(G, pos, thatNodes, node_color = 'r', linewidths = 0)
    #Draw normal nodes with shades of grey according to the distance
    for i in range(1, len(distRange)):
        thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['dist'] == i]
        nx.draw_networkx_nodes(G, pos, thatNodes, node_color = str(1 - (i * 1 / len(distRange))), linewidths = 0)
    #Draw the starting nodes
    #A list to be able to handle distances from a region
    thatStartNodes = [k for k in nx.nodes_iter(G) if G.node[k]['dist'] == 0]
    nx.draw_networkx_nodes(G, pos, thatStartNodes, node_color = 'y', linewidths = 0)

    nx.draw_networkx_edges(G, pos, edge_color = 'k')
    plt.show()
