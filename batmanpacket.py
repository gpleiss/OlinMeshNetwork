from packet import *
from random import *

class BATMANPacket(Packet):
	ogm=0
	ogm_origin=None
	ogm_ttl=0
	ogm_sequence=0
	ogm_sender=None

	def __init__(self):
		self.ogm=0
	
	def setOGM (self, node):
		self.ogm=1
		self.ogm_origin=node.id
		self.ogm_ttl=20
		self.ogm_sequence=node.ogm_sequence
		self.ogm_sender=node.id
	
	def setMSG (self, immediateDest, finalDest):
		self.set_nextDest(immediateDest)
		self.final=finalDest
	
	def isOGM (self):
		return ogm
	