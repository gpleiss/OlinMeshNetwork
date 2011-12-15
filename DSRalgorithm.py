'''
Created on Dec 14, 2011

@author: gpleiss
'''
from algorithm import Algorithm
import math
from random import randint
from meshgraph import MeshGraph
from algorithm import Algorithm

class DSRalgorithm(Algorithm):
    '''
    classdocs
    '''
    

    def __init__(self, g):
        '''
        Constructor
        '''
        Algorithm.__init__(self, g)
        self.table = {}        

            
            
    def xmit_msg(self, origin, dest):
        
        if self.g.nodes().count(origin) == 0:
            return (None, 0)
        
        # Flood network if path not in table, otherwise get path from table
        if self.table.get((origin, dest), None) == None:
            (path, transmissions) = self.find_path(origin, dest) 
            self.table[(origin, dest)] = path
        else:
            path = self.table[(origin, dest)]
            transmissions = 0
        
        # Break if no valid path
        # TODO: should resent
        if path == None:
            return (None, transmissions)
        # Transverse packet down path
        i = 0
        while i+1 < len(path):
            if self.g.neighbors(path[i]).count(path[i+1]) == 0:
                break
            else:
                transmissions += 1
                i += 1
        # If it made it to the path, return the path and the number of transmissions
        if path[i] == dest:
            return (path, transmissions)
        # If it didn't make it to the path, try the transmission again by reflooding
        # the network
        else:
            self.table.pop((origin, dest))
            return self.xmit_msg(origin, dest)
    
    
    
    
    def find_path(self, origin, dest):
        # flood the network
        transmissions=0
        flood={origin:origin} #{A:B} A was flooded from B.
        needsFlood={origin:True}
        
        while DSRalgorithm.util_DSR_Flood_Incomplete(needsFlood):
            for node in flood.keys():
                if needsFlood[node]==True:
                    needsFlood[node]=False
                    transmissions+=1
                    for adj_node in self.g.neighbors(node):
                        if flood.keys().count(adj_node)==0:
                            #We need to flood adj_node
                            flood[adj_node]=node
                            needsFlood[adj_node]=True
      
        if flood.keys().count(dest)==0:
            return (None,transmissions)
        
        # generate path now
        path=[dest]
        currNode=dest
        while currNode!=origin:
            path.append(flood[currNode])
            currNode=flood[currNode]
            transmissions+=1
        path.reverse()
        return (path, transmissions)
    
    @staticmethod
    def util_DSR_Flood_Incomplete(needsFlood):
        for node in needsFlood.keys():
            if needsFlood[node]:
                return True
        return False
            