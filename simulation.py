'''
Created on Dec 3, 2011

@author: gpleiss
'''
import networkx as nx
import matplotlib.pyplot as plt
from meshgraph import MeshGraph
from algorithm import Algorithm
from ahodv import Ahodv
import time
    
    
class Simulation():
    """ Simulation of an Algorithm on a MeshGraph
    """
    
    def __init__(self, g, Algo):
        """ Creates a simulation. Does not run it but sets it up.
            @param g: (MeshGraph) The graph that will be simulated on
            @param Algo: (ClassObject, subclass of Algorithm)
                The algorithm to simulate
        """
        self.g = g
        self.algo = Algo(g)
        if not isinstance(self.algo, Algorithm): 
            raise Exception("Algo must be a subclass of Algorithm")
            
    def __update_graph(self):
		""" Runs after each step in the simulation
			Make the graph display changes as a result of the algorithm
		"""
		
		nodes = self.g.nodes(data=True)
		pos = dict()
		for node in nodes:
			pos[node[0]] = node[1]['pos']
		nx.draw_networkx(self.g, pos, with_labels=True, node_color = [Simulation.__color(node) for node in nodes])
		plt.draw()
		#time.sleep(0.01)
		
    def start(self):
        """ Start the simulation
            @return: True if the simulation runs successfully
        """
        plt.ion()
        self.__update_graph()
        while self.algo.has_next_step():
            self.algo.next_step()
            self.__update_graph()
        plt.show()
        print(self.num_hop_list)
        return True
    
    @staticmethod
    def __color(node):
        state = node[1]['state']
        return {
            0: "blue",
            1: "red",
            2: "black",
            3: "green"}[state]


if __name__ == '__main__':
    g = MeshGraph(n_rows=7, n_cols=7, row_dist=2, col_dist=1, max_offset=0.25)
    s = Simulation(g, Ahodv)
    s.start()