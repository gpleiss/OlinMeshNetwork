from node import *
from batmanpacket import *

class BATMANNode(Node):
	routingTable=dict()
	routingQuality=dict()
	routingTableAge=0
	ogm_sequence=0
	
	def __init__(self, inId, allNodes = None):
		self.initNode(inId,allNodes)
		self.routingTable=dict.fromkeys(allNodes)
		self.routingQuality=dict.fromkeys(allNodes)
		self.genOGM()
		
	def genOGM (self):
		p=BATMANPacket()
		self.ogm_sequence=randint(0,2^16-1)
		p.setOGM(self)
		self.ogm_sequence++
		routingTableAge=0
		self.outQ.put(p)
		
	def rxPacket(self,packet):
		if (not(isInstance(packet,BATMANPacket))):
			return
		if (packet.isOGM()==0):
			if (packet.final==self.id):
				return
			else:
				if(packet.getNextDist()==self.id):
					p=BATMANPacket()
					p.setMSG(self.routingTable[packet.final],packet.final)
					self.outQ.put(p)
		else:
			if(packet.ogm_origin==self.id):
				return
			else:
				if(self.routingTable[packet.final]==None or self.routingQuality[packet.final]>packet.ogm_ttl):
					self.routingTable[packet.final]=packet.ogm_sender
					self.routingQuality[packet.final]=packet.ogm_ttl
				if(packet.ogm_ttl>0):
					packet.ogm_ttl--
					packet.ogm_sender=self.id
					self.outQ.put(packet)
		
	def txPacket(self):
		routingTableAge++
		if(routingTableAge>100):
			self.genOGM()
		return self.outQ.get()
	