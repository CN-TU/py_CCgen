from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.tls import *
from scapy.all import load_layer

class CovertChannel():
	def __init__(self, online, config, message):
		pass

	def modify(self, pkt, mappedvalue, params):
		if(mappedvalue != -1):
			load_layer("tls") 
			print(pkt.haslayer(TLS),mappedvalue)
			if pkt.haslayer(TLS):
			    #print(pkt[TLS].show2())
			    print(pkt[TLS][0].len)
			    pkt[TLS][0].len = int(mappedvalue)+int(params['poff'])
			    print(pkt[TLS][0].len)
		return pkt

	def extract(self, pkt, params):
		if pkt.haslayer(TLS):
			print(pkt[TLS][0].len)
			return int(pkt[TLS][0].len)-int(params['poff'])


