'''
Created on Dec 3, 2011

@author: gpleiss
'''
import networkx as nx
from random import random


class MeshGraph(nx.Graph):
    """ A graph representing a Wireless Mesh Network
    """
    
    PASSIVE = 0
    CNCTD = 1
    SENDING = 2
    ONPATH = 3
    
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
                self.add_node(v, pos=pos, state=MeshGraph.PASSIVE)
                if not i==0:
                    self.add_edge(v, self.get_node(i-1, j))
                if not j==0:
                    self.add_edge(v, self.get_node(i, j-1))
        self.root = self.nodes()[0]
        self.dest = self.nodes()[-1]

    def nodes(self, data=False):
        nodes_list = None
        if data == False:
            nodes_list = self.node.keys()
            nodes_list.sort()
            return nodes_list
        else:
            nodes_list = zip(self.node.keys(), self.node.values())
            nodes_list.sort()
            return nodes_list

    def get_node(self, x, y):
        """ Finds and returns the node in the graph at col x and row y
            @param x: (int) column of node to find
            @param y: (int) row of node to find
            @return: (string) name of node 
        """
        return "%c%i" % (chr(y + ord('A')), x+1)
    
    def get_node_state(self, node):
        return self.node[node]['state']
    
    def nodes_with_state(self, state):
        nodes_with_state = []
        for node in self.node.keys():
            if self.node[node]['state'] == state:
                nodes_with_state.append(node)
        return nodes_with_state
    
    def set_node_state(self, node, state):
        prev_state = self.node[node]['state']
        self.node[node]['state'] = state
        return True if prev_state != state else False
    
    def get_node_attr(self, node, attr):
        return self.node[node][attr]
    
    def set_node_attr(self, node, attr, val):
        self.node[node][attr] = val