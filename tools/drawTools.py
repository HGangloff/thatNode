import networkx as nx
import matplotlib.pyplot as plt
from random import random


def drawFromClasses(G, title = None): 
    '''
    Draws a binary graph with 2 different class in the 'class' attributes 
    TO DO : Rename in "drawBinaryGraph"
    '''
    pos = nx.get_node_attributes(G, 'pos')
    classes = nx.get_node_attributes(G, 'class')
    black_nodes = [k for k, v in classes.items() if v == 0]
    white_nodes = [k for k, v in classes.items() if v == 1]
    nx.draw_networkx_nodes(G, pos, black_nodes, node_color = '0', linewidths = 0)
    nx.draw_networkx_nodes(G, pos, white_nodes, node_color = '1', linewidths = 0.2)
    nx.draw_networkx_edges(G, pos, edge_color = 'k')
    if title:
        plt.title(title)
    plt.show()

def drawDistanceGraph(G, title = None):
    '''
    Given a decimal graph (with attribute 'dist') it draws the distance graph using nodes with dist = 0 as basis
    '''
    pos = nx.get_node_attributes(G, 'pos')
    dist = nx.get_node_attributes(G, 'dist')
    distRange = [v for k, v in dist.items() if v != float("inf")]
    distRange = list(set(distRange)) #kill duplicates
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
    if title:
        plt.title(title)
    plt.show()

def drawLabelledGraph(G, title = None):
    '''
    Given a decimal graph G it draws theconnected components (labels, or 'class' =/= 0) using different colors
    '''
    pos = nx.get_node_attributes(G, 'pos')
    dist = nx.get_node_attributes(G, 'dist')
    lblDict = nx.get_node_attributes(G, 'class')
    lblRange = lblDict[max(lblDict, key = lambda x: lblDict.get(x))]
    #Draws the nodes with no label
    thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == 0]
    nx.draw_networkx_nodes(G, pos, thatNodes, node_color = 'k', linewidths = 0)
    #Draws the labelled nodes
    for i in range(lblRange):
        thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == (i + 1)]
        r = random()
        v = random()
        b = random()
        color = (r, v, b) #Problem with coloring if 3 nodes in the connected component
        nx.draw_networkx_nodes(G, pos, thatNodes, node_color = color, linewidths = 0)
    nx.draw_networkx_edges(G, pos, edge_color = 'k')
    if title:
        plt.title(title)
    plt.show()

def drawZoneofIGraph(G, title = None):
    '''
    Draw the zone of influences graph G which is a decimal graph. Also connected components are labelled differently in 'class' and the zone of influence is nodes whose 'class' is = -label
    '''
    pos = nx.get_node_attributes(G, 'pos')
    dist = nx.get_node_attributes(G, 'dist')
    lblDict = nx.get_node_attributes(G, 'class')
    lblRange = lblDict[max(lblDict, key = lambda x: lblDict.get(x))]
    #Draws the nodes on the border of zones of influence
    thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == 0]
    nx.draw_networkx_nodes(G, pos, thatNodes, node_color = 'k', linewidths = 0)
    #Draws the labelled nodes (part of connected comp) and their zones of I
    alrdyDrawnEdges = []
    for i in range(lblRange):
        thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == (i + 1)]
        theirZI = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == -(i + 1)]
        allThatNodes = thatNodes + theirZI
        thatEdges = []
        for v in allThatNodes:
            for vv in allThatNodes:
                if G.has_edge(v, vv):
                    thatEdges.append((v, vv))
                    alrdyDrawnEdges.append((v, vv))
        r = random()
        v = random()
        b = random()
        color = (r, v, b) #Problem with coloring if 3 nodes in the connected component
        nx.draw_networkx_nodes(G, pos, thatNodes, node_color = color, linewidths = 0.2)
        nx.draw_networkx_nodes(G, pos, theirZI, node_color = color, linewidths = 0, alpha = 0.7)
        nx.draw_networkx_edges(G, pos, thatEdges, edge_color = 'k', alpha = 0.2) #Problem with edge_color = color ?
    #Draw the remaining edges
    remainingEdges = [e for e in G.edges() if e not in alrdyDrawnEdges]
    nx.draw_networkx_edges(G, pos, remainingEdges, edge_color = 'k')
    if title:
        plt.title(title)
    plt.show()

