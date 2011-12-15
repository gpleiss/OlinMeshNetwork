'''
Created on Dec 14, 2011

@author: gpleiss
'''
from algorithm import Algorithm
import operator
import math
import copy
from random import randint
from meshgraph import MeshGraph
from algorithm import Algorithm
import networkx as nx

class GLSRalgorithm(Algorithm):
	'''
	classdocs
	'''
	

	def __init__(self, g):
		'''
		Constructor
		'''
		Algorithm.__init__(self, g)
		self.old_g = nx.Graph()

			
			
	def xmit_msg(self, origin, dest):
		'''
		returns a tuple of path and transmissions
		''' 
		node_distance = {}
		prev_node = {}
		current_node = origin
		unvisited_nodes = {}
		shortestPath = []
		transmissions=self.repair()
		
		for node in self.g.nodes():
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
			
		return (shortestPath, transmissions+len(shortestPath)-1)
	
	def repair(self):
		transmissions=len(self.g.nodes()) #All the hellos.
		for n in self.g.nodes():
			if self.old_g.nodes().count(n)>0:
				new_neighborhood=self.g.neighbors(n)
				old_neighborhood=self.old_g.neighbors(n)
				transmittedLSA=False
				for neighbor in new_neighborhood:
					if old_neighborhood.count(neighbor)==0:
						(f,t)=Algorithm.util_flood(self.g,n)
						transmissions+=t
						transmittedLSA=True
						break
				if transmittedLSA:
					break
				for neighbor in old_neighborhood:
					if new_neighborhood.count(neighbor)==0:
						(f,t)=Algorithm.util_flood(self.g,n)
						transmissions+=t
						break
			else:
				(f,t)=Algorithm.util_flood(self.g, n)
				transmissions+=t
		self.old_g=copy.deepcopy(self.g)
		return transmissions
			