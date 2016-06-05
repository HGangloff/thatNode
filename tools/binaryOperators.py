import networkx as nx

def binaryAdd(G1, G2):
    '''
    "Adds" G1 and G2 on their 'class' attribute
    '''
    Gout = G1.copy()
    for v in nx.nodes_iter(Gout):
        Gout.node[v]['class'] = G1.node[v]['class'] + G2.node[v]['class']
        if Gout.node[v]['class'] == 2:
            Gout.node[v]['class'] = 1
    
    return Gout

def binarySub(G1, G2):
    '''
    "Substracts" G2 to G1 on their 'class' attribute
    '''
    Gout = G1.copy()
    for v in nx.nodes_iter(Gout):
        Gout.node[v]['class'] = G1.node[v]['class'] - G2.node[v]['class']
        if Gout.node[v]['class'] == -1:
            Gout.node[v]['class'] = 0

    return Gout

def binaryOr(G1, G2):
    '''
    Performs an OR on the attribute 'class' of G1 and G2.
    Equivalent to an union
    '''
    Gout = G1.copy()
    for v in nx.nodes_iter(Gout):
        Gout.node[v]['class'] = 0
        if G1.node[v]['class'] == 1 or G2.node[v]['class'] == 1:
            Gout.node[v]['class'] = 1

    return Gout

def binaryAnd(G1, G2):
    '''
    Perform an AND on the attribute 'class' of G1 and G2.
    Equivalent to an intersection
    '''
    Gout = G1.copy()
    for v in nx.nodes_iter(Gout):
        Gout.node[v]['class'] = 0
        if G1.node[v]['class'] == 1 and G2.node[v]['class'] == 1:
            Gout.node[v]['class'] = 1

    return Gout
