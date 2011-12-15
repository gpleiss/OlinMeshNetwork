'''
Created on Dec 3, 2011

@author: gpleiss
'''
from meshgraph import MeshGraph
from random import random, randint
from collections import deque

class Algorithm():
    """ An algorithm to be performed on a MeshGraph.
        To run the algorithm, each step should be implemented by
            running the method next_step, until there are no more 
            steps remaining (which can be determined by the method 
            has_next_step)
    """	
    @staticmethod
    def util_flood(graph, origin):
		transmissions=0
		flood={origin:origin} #{A:B} A was flooded from B.
		needsFlood={origin:True}
        
		while Algorithm.util_flood_incomplete(needsFlood):
			for node in flood.keys():
				if needsFlood[node]==True:
					needsFlood[node]=False
					transmissions+=1
					for adj_node in graph.neighbors(node):
						if flood.keys().count(adj_node)==0:
							#We need to flood adj_node
							flood[adj_node]=node
							needsFlood[adj_node]=True
		return (flood,transmissions)
        
    @staticmethod
    def util_flood_incomplete(needsFlood):
        for node in needsFlood.keys():
            if needsFlood[node]:
                return True
        return False
    
    def __init__(self, g):
        """ Creates an instance that contains a MeshGraph for the
                algorithm to be run on
            @param g: (MeshGraph) The graph to run the algo on
        """
        self.g = g
        
        self.MSG_PERIOD = 2
        self.REPAIR_PERIOD = 5
        self.DEL_PERIOD = 2
        self.ADD_PERIOD = 2
        self.RETRY_PERIOD = 1
        
        self.DEL_PROB = .45
        self.ADD_PROB = .55
        self.MAX_RETRIES = 3
        
        self.removed_nodes = {}
        self.retry_queue = deque()
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
        new_data = {}
        num_repair_trans = 0
        self.time += 1
        [self.g.set_node_state(node, MeshGraph.PASSIVE) for node in self.g.nodes()] 
        
                
        if self.time % self.DEL_PERIOD == 0:
            if random() <= self.DEL_PROB:
                nodes = self.g.nodes()
                node = self.remove_node(nodes[randint(0, len(nodes)-1)])
                print "Deletion. Removed: %s" % (node)


        if self.time % self.ADD_PERIOD == 0:
            n = len(self.removed_nodes.keys())
            if n > 0 and random() <= self.ADD_PROB:
                node = self.restore_node(self.removed_nodes.keys()[randint(0, n-1)])
                print "Add. Added: %s" % (node)
                
                
        if self.time % self.RETRY_PERIOD == 0:
            if len(self.retry_queue) > 0:
                ((origin, dest), data) = self.retry_queue.popleft()
                num_tries = data['num_tries']
                total_trans = data['trans']
                num_tries += 1
            
                (path, new_trans) = self.xmit_msg(origin, dest)
                total_trans += new_trans
                print "Retry #%i. Origin: %s, Dest: %s, Transmissions: %i" % (
                        num_tries, origin, dest, total_trans),
                
                if path != None:
                    [self.g.set_node_state(node, MeshGraph.ONPATH) for node in path]
                    print "SUCCESS"
                    new_data[total_trans] = new_data.get(total_trans, 0) + 1
                else:
                    if num_tries < self.MAX_RETRIES:
                        self.retry_queue.append(((origin, dest), {
                                'num_tries':num_tries, 'trans':total_trans}))
                        print "FAILED"
                    else:
                        print "FAILED (no more attempts)"
                        new_data[total_trans] = new_data.get(total_trans, 0) + 1
                        
                
        if self.time % self.MSG_PERIOD == 0:
            if self.g.nodes().count(origin) == 0:
                (path, trans) = (None, 0)
            else:
                (origin, dest) = self.get_origin_and_dest()
                (path, trans) = self.xmit_msg(origin, dest)
            print "Message. Origin: %s, Dest: %s, Transmissions: %i" % (origin, dest, trans),
            
            if path != None:
                [self.g.set_node_state(node, MeshGraph.ONPATH) for node in path]
                print "SUCCESS"
                new_data[trans] = new_data.get(trans, 0) + 1
            else:
                self.retry_queue.append(((origin, dest), {'num_tries': 0, 'trans':trans}))
                print "FAILED"
            
            
        if self.time % self.REPAIR_PERIOD == 0:
            trans = self.repair()
            num_repair_trans += trans
            print "Repair. Transmissions: %i" % (trans)
                
                
        return (new_data, num_repair_trans)
                
                
                
    def get_origin_and_dest(self, rand_origin=True, rand_dest=False):
        nodes = self.g.nodes()
        origin = nodes[randint(0, len(nodes)-1)] if rand_origin else nodes[0]
        if rand_dest:
            dest = origin
            while dest == origin:
                dest = nodes[randint(0, len(nodes)-1)]
        else: dest = self.g.nodes()[-1]
        return (origin, dest)
    
    
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

