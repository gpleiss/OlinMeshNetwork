'''
Created on Dec 14, 2011

@author: gpleiss
'''
import simulation, pmf, cdf
import matplotlib.pyplot as plt
from meshgraph import MeshGraph
from DSRalgorithm import DSRalgorithm

class DataSimulation(simulation.Simulation):
    
    def __init__(self, g, Algo):
        simulation.Simulation.__init__(self, g, Algo)
        self.hist = pmf.Hist()
        
    
    def start(self):
        """ Start the simulation
            @return: True if the simulation runs successfully
        """
        i = 0
        while self.algo.has_next_step() and i < 10000:
            new_data = self.algo.next_step()
            for num_trans, num_occur in zip(new_data.keys(), new_data.values()):
                self.hist.Incr(num_trans, num_occur)
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