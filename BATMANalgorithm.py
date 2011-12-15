'''
Created on Dec 14, 2011

@author: gpleiss
'''
from algorithm import Algorithm
import math
from random import randint
from meshgraph import MeshGraph
from algorithm import Algorithm

class BATMANalgorithm(Algorithm):
	def __init__(self, g):
		Algorithm.__init__(self, g)
		self.tables={}

	def xmit_msg(self, origin, dest):
		#tables should be {A:{B:?,C:?,D:?},B:{A:?,C:?,D:?},...}
		#that is, it is first a dict mapping a node name to its routing table:
		#   routing table is where to go (value) to reach the destination node (key)
		self.repair()
		transmissions=0
		currNode=origin
		path=[currNode]
		while not currNode==dest:
			routeTable=self.tables[currNode]
			if routeTable.get(dest)==None:
				return (None,2*transmissions)
			else:
				currNode=routeTable[dest]
				transmissions+=1
				path.append(currNode)
		return (path, transmissions)

	def repair(self):
		#returns out a tuple of (tables, transmissions)
		#call this function periodically.
		self.tables={}
		transmissions=0
		#init tables
		for node in self.g.nodes():
			self.tables[node]={}
		#sender_node generates an OGM
		for sender_node in self.g.nodes():
			(flood,t)=Algorithm.util_flood(self.g,sender_node)
			transmissions+=t
			for adj_node in flood.keys():
				self.tables[adj_node][sender_node]=flood[adj_node]
		
		return transmissions
			