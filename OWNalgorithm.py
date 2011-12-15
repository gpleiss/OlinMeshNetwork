'''
Created on Dec 14, 2011

@author: gpleiss
'''
from algorithm import Algorithm
import math
from random import randint
from meshgraph import MeshGraph
from algorithm import Algorithm

class OWNalgorithm(Algorithm):
	'''
	classdocs
	'''
	

	def __init__(self, g):
		'''
		Constructor
		'''
		Algorithm.__init__(self, g)
		self.tables = {}		
		#init tables
		for node in self.g.nodes():
			self.tables[node]={}

	def find_path(self, origin, dest):
		# flood the network
		transmissions=0
		(flood,t)=Algorithm.util_flood(self.g,origin)
		transmissions+=t
	  
		if flood.keys().count(dest)==0:
			return (None,transmissions)
		
		# generate path now
		path=[dest]
		currNode=dest
		while currNode!=origin:
			path.append(flood[currNode])
			currNode=flood[currNode]
			transmissions+=1
		path.reverse()
		return (path, transmissions)
			
	def xmit_msg(self, origin, dest):
		self.trans=0
		p=self.xmit_msg_real(origin,dest)
		return (p,self.trans)
		
	def xmit_msg_real(self, currNode, dest, pathin=None):
		#basic premise: the data is flooded if there is no path.
		#we have self.tables same as BATMAN.
		#need self.tables to contain an empty dict for each node.
		#INIT self.trans=0 before calling!

		#Data tx'd with control.
		if (not pathin==None) and pathin.count(currNode)>0:
			(p,t)=self.find_path(currNode, dest)
			if p==None:
				return None
			self.util_OWN_Record_Path(p)
			self.trans+=t
			path.pop()
			path.extend(p)
			return path
		if pathin==None:
			path=[currNode]
		else:
			path=pathin
			path.append(currNode)
		if currNode==dest:
			return path
		table=self.tables[currNode]
		if table.keys().count(dest)>0:
			self.trans+=1 #counts the Tx msg
			nextNode=table[dest]
			if self.g.neighbors(currNode).count(nextNode)>0:
				#elf.trans+=1 #counts the ACK msg.
				return self.xmit_msg_real(nextNode, dest, path)
		#don't have a route via tables. Route via DSR.
		(p,t)=self.find_path(currNode, dest)
		if p==None:
			return None
		self.util_OWN_Record_Path(p)
		self.trans+=t
		path.pop()
		path.extend(p)
		return path
		
	def util_OWN_Record_Path(self, path):
		for i in range(len(path)):
			if i<len(path)-1:
				self.tables[path[i]][path[len(path)-1]]=path[i+1]
			if i>0:
				self.tables[path[i]][path[0]]=path[i-1]
