'''
Created on Dec 3, 2011

@author: gpleiss
'''
import networkx as nx
from random import random


class MeshGraph(nx.Graph):
    """ A graph representing a Wireless Mesh Network
    """
    
    def __init__(self, n_rows, n_cols, row_dist, col_dist, max_offset=0):
        """ Creates a approximatly square mesh. Randomness factor prevents
            the graph from being perfectly square
            @param n_rows: (int) Number of rows of vertices on graph
            @param n_cols: (int) Number of cols
            @param row_dist: (float) Distance between rows
            @param col_dist: (float) Distance between cols
            @param max_offset: (float) Maximum amount that any vertex can 
                be off of exact position (measured by percent) 
        """
        super(nx.Graph, self).__init__()
        self.adj = {}
        self.node = {}
        for i in range(n_cols):
            for j in range(n_rows):
                v = self.get_node(i, j)
                x_off = (random() - 0.5) * 2*max_offset
                y_off = (random() - 0.5) * 2*max_offset
                pos = (col_dist*(i+x_off) , row_dist*(n_rows-j+y_off))
                self.add_node(v, pos=pos, active=False)
                self.add_edge(v, self.get_node(i-1, j)) if not i==0 else None
                self.add_edge(v, self.get_node(i, j-1)) if not j==0 else None
        print self.node
    
    
    def get_node(self, x, y):
        """ Finds and returns the node in the graph at col x and row y
            @param x: (int) column of node to find
            @param y: (int) row of node to find
            @return: (string) name of node 
        """
        return "%c%i" % (chr(y + ord('A')), x+1)
    
    def activate_node(self, node):
        """ Activates a given node (abstract -- represented a different
                state for the node)
            Node remains active until deactivate_node is called
            @return: (boolean) True if node was activated, False is
                node was already active
        """
        prev_state = self.node[node]['active']
        self.node[node]['active'] = True
        return True if prev_state == False else True
        
    def deactivate_node(self, node):
        """ Deactivates a given node (abstract -- represented a different
                state for the node)
            @return: (boolean) True if node was deactivated, False is
                node was already deactive
        """
        prev_state = self.node[node]['active']
        self.node[node]['active'] = False
        return True if prev_state == True else False
    
