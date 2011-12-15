
import pmf, cdf
import matplotlib.pyplot as plt
from meshgraph import MeshGraph
from data_simulation import DataSimulation
from DSRalgorithm import DSRalgorithm
from BATMANalgorithm import BATMANalgorithm
from OWNalgorithm import OWNalgorithm
from GLSRalgorithm import GLSRalgorithm


g = MeshGraph(n_rows=5, n_cols=5, row_dist=1, col_dist=1, max_offset=0.25)



AlgoClass = BATMANalgorithm
s = DataSimulation(g, AlgoClass)

#histograms = {}

fail_prob = .25
s.algo.DEL_PERIOD = 1
s.algo.ADD_PERIOD = 1
s.algo.DEL_PROB = fail_prob
s.algo.ADD_PROB = fail_prob + 0.08
s.hist = pmf.Hist()
s.start()
#histograms[fail_prob] = s.hist
    
legend_entries = []
lines = []
plt.Figure()
plt.hold(True)

#zipped_data = zip(histograms.keys(), histograms.values())
#zipped_data.sort()
#for (fail_prob, hist) in zipped_data:
data = pmf.MakePmfFromHist(s.hist)
(xs, ps) = data.Render()
#    legend_entries.append("Node failure prob = %.2f" % (fail_prob))
plt.subplot(1,2,1)
lines.append(plt.plot(xs, ps, linewidth=2))
#plt.legend(tuple(lines), tuple(legend_entries))
plt.xlim((0,50))
plt.subplot(1,2,2)
plt.plot(xs, ps, linewidth=2)
plt.xlim((400,650))
plt.xlabel("Number of transmissions")
plt.ylabel("P(x)")
#plt.title("""Network size: 5x5
#             Probability that a node fails per cycle: .25
#          """)
plt.show()
