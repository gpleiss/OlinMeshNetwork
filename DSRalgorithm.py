'''
Created on Dec 14, 2011

@author: gpleiss
'''
from algorithm import Algorithm
import math
from random import randint
from meshgraph import MeshGraph

class DSRalgorithm(Algorithm):
    '''
    classdocs
    '''
    TRANS_PERIOD = 10
    DISASTER_PERIOD = 2
    POSITIVE_PERIOD = 0
    

    def __init__(self, g):
        '''
        Constructor
        '''
        self.g = g
        self.g.remove_node('G7')
        self.table = {}
        
        self.time = 0
        
        self.__nodes = self.g.nodes()
    
    def has_next_step(self):
        return True
    
    def next_step(self):
        self.DSR_Find_Path(self.__nodes[0], 'G7')
    
    '''
    def next_step(self):
        self.time += 1
        
        # Transmission
        if self.time % DSRalgorithm.TRANS_PERIOD == 0:
            o = self.__nodes[randint(0, len(self.__nodes))]
            d = o
            while d == 0:
                d = self.__nodes[randint(0, len(self.__nodes))]
            (path, tot_trans) = self.DSR_Xmit_info(o, d)
            
            
        # Break something
        if self.time % DSRalgorithm.DISASTER_PERIOD:
            pass
    ''' 
            
    def DSR_Find_Path(self, origin, dest):
        print origin
        transmissions=0
        flood={origin:origin} #{A:B} A was flooded from B.
        needsFlood={origin:True}
        while DSRalgorithm.util_DSR_Flood_Incomplete(needsFlood):
            print "in while loop"
            for node in flood.keys():
                needsFlood[node]=False
                for adj_node in self.g.neighbors(node):
                    if flood.keys().count(adj_node)==0:
                        #We need to flood adj_node
                        flood[adj_node]=node
                        needsFlood[adj_node]=True
                        transmissions+=1
       
        if flood.keys().count(dest)==0:
            return None
       
        #generate path now.
        path=[dest]
        currNode=dest
        while currNode!=origin:
            path.append(flood[currNode])
            self.g.set_node_state(currNode, MeshGraph.ONPATH)
            currNode=flood[currNode]
            transmissions+=1
        self.g.set_node_state(currNode, MeshGraph.ONPATH)
        path.reverse()
        print path, transmissions
        print dest
        return (path, transmissions)
    
    @staticmethod
    def util_DSR_Flood_Incomplete(needsFlood):
        for node in needsFlood.keys():
            if needsFlood[node]:
                return True
        return False
            