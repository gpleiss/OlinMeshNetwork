'''
Created on Dec 11, 2011

@author: travisjlewis
'''

from Queue import *

class Node():
	""" A node object to be used in the simulation
	"""
	
	inQ = Queue()
	outQ = Queue()
	allNodes = list()
	id = None
	
	def initNode(self, inId, inAllNodes = None):
		self.id = inId
		self.allNodes = inAllNodes
		
	def hasTxPacket(self):
		return not(outQ.Empty())
		
	def rxPacket(self,packet):
		if self.id == packet.get_nextDist():
			outQ.put(packet)
		
	def txPacket(self):
		return outQ.get()