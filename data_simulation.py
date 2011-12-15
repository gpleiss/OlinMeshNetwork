'''
Created on Dec 14, 2011

@author: gpleiss
'''
import simulation, pmf, cdf
import matplotlib.pyplot as plt
from meshgraph import MeshGraph
from DSRalgorithm import DSRalgorithm
from BATMANalgorithm import BATMANalgorithm
from OWNalgorithm import OWNalgorithm
from GLSRalgorithm import GLSRalgorithm


class DataSimulation(simulation.Simulation):
    
    def __init__(self, g, Algo):
        simulation.Simulation.__init__(self, g, Algo)
        self.hist = pmf.Hist()
        
    
    def start(self):
        """ Start the simulation
            @return: True if the simulation runs successfully
        """
        i = 0
        max_time = 25000
        
        while self.algo.has_next_step() and i < max_time:
            num_trans = self.algo.next_step()
            self.hist.Incr(num_trans) if num_trans != 0 else None
            i += 1
    
    
    def plot_data(self):
        plt.Figure()
        data = pmf.MakePmfFromHist(self.hist)
#        data = cdf.MakeCdfFromHist(self.hist)
        (xs, ps) = data.Render()
        plt.plot(xs, ps)
        plt.show()


if __name__ == '__main__':
    g = MeshGraph(n_rows=5, n_cols=5, row_dist=1, col_dist=1, max_offset=0.25)
    s = DataSimulation(g, DSRalgorithm)
    s.start()
    s.plot_data()