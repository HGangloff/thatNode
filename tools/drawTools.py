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
    nx.draw_networkx(G, pos, with_labels = False)
    nx.draw_networkx_nodes(G, pos, black_nodes, node_color = '0', linewidths = 0)
    nx.draw_networkx_nodes(G, pos, white_nodes, node_color = '1', linewidths = 0)
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
    nx.draw_networkx(G, pos, with_labels = False)
    #Draws the nodes with no label
    thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == 0]
    nx.draw_networkx_nodes(G, pos, thatNodes, node_color = 'k', linewidths = 0)
    #Draws the labelled nodes
    for i in range(lblRange):
        thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == (i + 1)]
        r = random()
        v = random()
        b = random()
        color = (r, v, b) #bad coloring if connected component of size 3
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
    nx.draw_networkx(G, pos, with_labels = False)
    #Draws the nodes on the border of zones of influence
    thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == 0]
    nx.draw_networkx_nodes(G, pos, thatNodes, node_color = 'k', linewidths = 0)
    #Draws the labelled nodes (part of connected comp) and their zones of I
    for i in range(lblRange):
        thatNodes = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == (i + 1)]
        theirZI = [k for k in nx.nodes_iter(G) if G.node[k]['class'] == -(i + 1)]
        r = random()
        v = random()
        b = random()
        color = (r, v, b)
        color2 = (min(r + 0.3, 1), min(v + 0.3, 1), min(b + 0.3, 1))
        nx.draw_networkx_nodes(G, pos, thatNodes, node_color = color, linewidths = 0)
        nx.draw_networkx_nodes(G, pos, theirZI, node_color = color2, linewidths = 0)
    nx.draw_networkx_edges(G, pos, edge_color = 'k')
    if title:
        plt.title(title)
    plt.show()

