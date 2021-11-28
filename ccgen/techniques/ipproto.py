from scapy.layers.inet import IP

class CovertChannel():
	def __init__(self, online, config, message):
		pass

	def modify(self, pkt, mappedvalue, params):
		if(mappedvalue != -1):
			pkt[IP].proto = int(mappedvalue)
		return pkt

	def extract(self, pkt, params):
		return int(pkt[IP].proto)
