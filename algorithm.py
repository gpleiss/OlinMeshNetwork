'''
Created on Dec 3, 2011

@author: gpleiss
'''

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
        self.__nodes = self.g.nodes()
        self.__nodes.sort()
        self.__i = 0
        
    def has_next_step(self):
        """ @return: True, if the algorithm is not complete
                False, if there are still steps of the algorithm to run
        """
        return self.__i < len(self.__nodes)
    
    def next_step(self):
        """ Performs the next step of the algorithm on the MeshGraph
            @raise Exception: if the algorithm has no more steps remaining 
        """
        if not self.has_next_step():
            raise Exception("No more steps of the algorithm!")
        self.g.deactivate_node(self.__nodes[self.__i-1]) if self.__i>0 else None
        self.g.activate_node(self.__nodes[self.__i])
        self.__i += 1
