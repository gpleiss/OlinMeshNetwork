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
        max_time = 10000
        repair_trans = 0
        new_hist = pmf.Hist()
        
        while self.algo.has_next_step() and i < max_time:
            (new_data, new_repair_trans) = self.algo.next_step()
            repair_trans += new_repair_trans
            for num_trans, num_occur in zip(new_data.keys(), new_data.values()):
                new_hist.Incr(num_trans, num_occur)
            i += 1
        repair_offset = repair_trans/max_time
        for (key, val) in zip(new_hist.GetDict().keys(), new_hist.GetDict().values()):
            self.hist.Incr(key + repair_offset, val)
        print repair_offset
    
    
    def plot_data(self):
        plt.Figure()
        data = pmf.MakePmfFromHist(self.hist)
#        data = cdf.MakeCdfFromHist(self.hist)
        (xs, ps) = data.Render()
        plt.plot(xs, ps)
        plt.show()


if __name__ == '__main__':
    g = MeshGraph(n_rows=5, n_cols=5, row_dist=1, col_dist=1, max_offset=0.25)
    s = DataSimulation(g, BATMANalgorithm)
    s.start()
    s.plot_data()