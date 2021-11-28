from os.path import exists
from re import match
import itertools

class Message():
	def __init__(self, messagefile, n):
		if not exists(messagefile):
			raise Exception("ERROR: Messagefile does not exist")

		with open(messagefile, 'r+') as f:
			message = f.readline().rstrip('\n')
			assert match('^[01]+$', message), 'Invalid message: "%s"' % message

		self._message = self.cycle(message)
		self._n = n
		self.message = message

	def getdatagram (self):
		# get the next n bits and wrap around
		return "".join(itertools.islice(self._message, self._n))

	def cycle(self, iterable):
		# returns bits of a message one by one. When the message ends, return None
		for element in iterable:
			yield element

	def necessary_packets (self):
		# get the number of necessary packets to transmit the whole message
		return int(len(self.message)/self._n)
