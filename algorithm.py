'''
Created on Dec 3, 2011

@author: gpleiss
'''
from meshgraph import MeshGraph
from random import random, randint

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
        
        self.MSG_PERIOD = 1
        self.REPAIR_PERIOD = 5
        self.DEL_PERIOD = 2
        self.ADD_PERIOD = 2
        self.RETRY = 3
        
        self.DEL_PROB = .5
        self.ADD_PROB = .5
        
        self.removed_nodes = {}
        self.time = 0

    
        
    def has_next_step(self):
        """ @return: True, if the algorithm is not complete
                False, if there are still steps of the algorithm to run
        """
        return True
    
    def next_step(self):
        """ Performs the next step of the algorithm on the MeshGraph
            @raise Exception: if the algorithm has no more steps remaining 
        """
        self.time += 1
        [self.g.set_node_state(node, MeshGraph.PASSIVE) for node in self.g.nodes()] 
        
        if self.time % self.MSG_PERIOD == 0:
            (origin, dest) = self.get_origin_and_dest()
            (path, trans) = self.xmit_msg(origin, dest)
            if path != None:
                [self.g.set_node_state(node, MeshGraph.ONPATH) for node in path]
            print "Message. Origin: ", origin, ", Destination: ", dest,
            print ", tramsissions: ", trans
            
            
        if self.time % self.REPAIR_PERIOD == 0:
            trans = self.repair()
            print "Repair. Transmissions: ", trans
        
        
        if self.time % self.DEL_PERIOD == 0:
            if random() >= self.DEL_PROB:
                nodes = self.g.nodes()
                node = self.remove_node(nodes[randint(1, len(nodes)-2)])
                print "Deletion. Removed: ", node


        if self.time % self.ADD_PERIOD == 0:
            n = len(self.removed_nodes.keys())
            if n > 0 and random() >= self.ADD_PROB:
                node = self.restore_node(self.removed_nodes.keys()[randint(0, n-1)])
                print "Add. Added: ", node
                
                
                
    def get_origin_and_dest(self):
        return ('A1', 'E5')    
    
    def xmit_msg(self, origin, dest):
        return (None, 0) 
    
    def repair(self):
        return 0
           
                
    def remove_node(self, node):
        pos = dict(self.g.nodes(data=True))[node]['pos']
        adj_nodes = self.g.neighbors(node)
        self.g.remove_node(node)
        self.removed_nodes[node] = {'pos':pos, 'adj_nodes':adj_nodes}
        return node

        
    def restore_node(self, node):
        if self.removed_nodes.has_key(node):
            data = self.removed_nodes.pop(node)
            self.g.add_node(node, pos=data['pos'], state=MeshGraph.PASSIVE)
            for adj_node in data['adj_nodes']:
                if adj_node in self.g.nodes(): # Adjacent node is on the graph
                    self.g.add_edge(node, adj_node) 
                else: # Adjacent node has been removed from the graph
                    self.removed_nodes[adj_node]['adj_nodes'].append(node)
        return node


