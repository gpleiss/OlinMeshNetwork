'''
Created on Dec 3, 2011

@author: gpleiss
'''
import networkx as nx
import matplotlib.pyplot as plt
from meshgraph import MeshGraph
from algorithm import Algorithm
from DSRalgorithm import DSRalgorithm
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
        self.num_hop_list = list()
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
    
    def start(self):
        """ Start the simulation
            @return: True if the simulation runs successfully
        """
        plt.ion()
        self.__update_graph()
        for i in range(2):
            while self.algo.has_next_step():
                self.algo.next_step()
                self.__update_graph()
            self.num_hop_list.append(self.algo.get_num_hops())
            self.algo.create_new_packet()
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