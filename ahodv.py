'''
Created on Dec 7, 2011

@author: gpleiss
'''
from algorithm import Algorithm
from meshgraph import MeshGraph
from random import randint
from collections import deque

class Ahodv(Algorithm):
    
    def __init__(self, g, timeout=20):
        self.g = g
        self.timeout = timeout
        self.__nodes = self.g.nodes()
        self.__cnct_by = {}
        self.__path = deque()
        self.num_hops = 0
        
        self.g.set_node_state(self.g.root, MeshGraph.SENDING)
        self.g.dest = self.__nodes[randint(0, len(self.__nodes)-1)]
        print self.g.dest
        
    def has_next_step(self):
        if len(self.__path) > 0 and self.__path[0] == self.g.root:
            return False
        return True
    
    def next_step(self):
        
        # If destination node has been found, retrace back path to root
        if len(self.__path) > 0:
            prev_node = self.__cnct_by.get(self.__path[0], None)
            if not prev_node == None:
                self.g.set_node_state(prev_node, MeshGraph.ONPATH)
                self.__path.appendleft(prev_node)
        
        # Have nodes propagate back once path has been established
        for node in self.g.nodes_with_state(MeshGraph.SENDING):
            for adj_node in self.g.neighbors(node):
                if self.g.get_node_state(adj_node) == MeshGraph.PASSIVE:
                    if adj_node == self.g.dest:
                        self.g.set_node_state(adj_node, MeshGraph.ONPATH)
                        self.__path.appendleft(adj_node)
                    else:
                        self.g.set_node_state(adj_node, MeshGraph.SENDING)
                        self.g.node[adj_node]
                    self.__cnct_by[adj_node] = node
            self.g.set_node_state(node, MeshGraph.CNCTD)
            
        # Time out nodes that have been around for too long
        # for node in self.g.nodes_with_state(MeshGraph.CNCTD):
            # self.g.node[node]['time'] = self.g.node[node].get('time', 0) + 1
            # if self.g.node[node]['time'] >= self.timeout:
                # self.g.set_node_state(node, MeshGraph.PASSIVE)
                # self.__cnct_by.pop(node, None)
        
        self.num_hops = self.num_hops + 1
        # Still need to include hops number?
        # Only works for single packet
	
    def get_num_hops(self):
        return self.num_hops
        
    def create_new_packet(self):
        self.num_hops = 0
        self.__path.clear()
        self.g.set_node_state(self.g.root, MeshGraph.SENDING)
        self.g.dest = self.__nodes[randint(0, len(self.__nodes)-1)]
        
        for node in self.g.node:
            self.g.set_node_state(node, MeshGraph.PASSIVE)
        
        self.g.set_node_state(self.g.root, MeshGraph.SENDING)
        print self.g.dest