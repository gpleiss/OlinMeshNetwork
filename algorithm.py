'''
Created on Dec 3, 2011

@author: gpleiss
'''
from meshgraph import MeshGraph
from random import randint

class Algorithm():
    """ An algorithm to be performed on a MeshGraph.
        To run the algorithm, each step should be implemented by
            running the method next_step, until there are no more 
            steps remaining (which can be determined by the method 
            has_next_step)
    """
    
    def __init__(self, g):
        """ Creates an instance that contains a MeshGraph for the
                algorithm to be run on
            @param g: (MeshGraph) The graph to run the algo on
        """
        self.g = g
        
        self.TRANS_PERIOD = 1
        self.DISASTER_PERIOD = 2
        self.RESTORE_PERIOD = 2
        
        self.removed_nodes = {}
        self.time = 0
        
    def remove_node(self, node):
        pos = dict(self.g.nodes(data=True))[node]['pos']
        adj_nodes = self.g.neighbors(node)
        self.g.remove_node(node)
        self.removed_nodes[node] = {'pos':pos, 'adj_nodes':adj_nodes}

        
    def restore_node(self, node):
        if self.removed_nodes.has_key(node):
            data = self.removed_nodes.pop(node)
            self.g.add_node(node, pos=data['pos'], state=MeshGraph.PASSIVE)
            for adj_node in data['adj_nodes']:
                if adj_node in self.g.nodes(): # Adjacent node is on the graph
                    self.g.add_edge(node, adj_node) 
                else: # Adjacent node has been removed from the graph
                    self.removed_nodes[adj_node]['adj_nodes'].append(node)
                    
    def get_origin_and_dest(self):
        return ('A1', 'E5')
    
        
    def has_next_step(self):
        """ @return: True, if the algorithm is not complete
                False, if there are still steps of the algorithm to run
        """
        return False
    
    def next_step(self):
        """ Performs the next step of the algorithm on the MeshGraph
            @raise Exception: if the algorithm has no more steps remaining 
        """
        self.time += 1
        nodes = self.g.nodes()        
        [self.g.set_node_state(node, MeshGraph.PASSIVE) for node in nodes] 
        
        if 1 == randint(1, self.DISASTER_PERIOD):
            self.remove_node(nodes[randint(1, len(nodes)-2)])

        n = len(self.removed_nodes.keys())
        if 1 == randint(1, self.RESTORE_PERIOD) and n > 0:
            self.restore_node(self.removed_nodes.keys()[randint(0, n-1)])

