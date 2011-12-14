import operator
from algorithm import Algorithm

class GLSR(Algorithm):
    
    def __init__(self, g):
        '''
        Constructor
        '''
        self.g = g
        self.g.remove_node('G7')
        self.time = 0
        
        self.__nodes = self.g.nodes()
        
    def has_next_step(self):
        return True
    
    def next_step(self):
        self.GLSR_Message(self.g, 'A1', 'G3')
        
    def GLSR_Message(self, g, origin, dest):
        '''
        returns a tuple of path and transmissions
        ''' 
        node_distance = {}
        prev_node = {}
        current_node = origin
        unvisited_nodes = {}
        shortestPath = []
        shortestLength = len(shortestPath) - 1
        
        for node in g.nodes():
            node_distance[node] = 99999 #simulate infinity
            prev_node[node] = None
            unvisited_nodes[node] = 1
            
        node_distance[origin] = 0
        
        while len(unvisited_nodes.keys()) != 0:
            current_node = min(node_distance.iteritems(), key=operator.itemgetter(1))[0]
            if node_distance[current_node] == 99999:
                break
            
            if current_node == dest:
                break
            
            for adj_node in self.g.neighbors(current_node):
                if adj_node in unvisited_nodes.keys():
                    alt = node_distance[current_node] + 1
                    if alt < node_distance[adj_node]:
                        node_distance[adj_node] = alt
                        prev_node[adj_node] = current_node
            
            del(node_distance[current_node])
            del(unvisited_nodes[current_node])
            
        u = dest
        while u in prev_node.keys():
            shortestPath.append(u)
            u = prev_node[u]
            
        return (shortestPath, shortestLength)
            