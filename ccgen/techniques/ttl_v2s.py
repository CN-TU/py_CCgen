from scapy.layers.inet import IP

class CovertChannel():
	def __init__(self, online, config, message):
		pass

	def modify(self, pkt, mappedvalue, params):
		if (mappedvalue != -1):
			pkt[IP].ttl = int(mappedvalue)
		return pkt

	def extract(self, pkt, params):
		return pkt[IP].ttl
