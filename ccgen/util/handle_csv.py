import csv

def chunkstring(string, length):
    chunks = [string[i:i+length] for i in range(0, len(string), length)]
    return chunks 

class Mapping():
	def __init__(self, mappingFile, bits):
		csv_f = csv.reader(open(mappingFile))

		self._b2n_func = False
		self._b2n_size = None
		self._filename = mappingFile
		self._data2mapping = {}
		self._mapping2data = {}
		self.param = {}

		for row in csv_f:
			if len(row) < 2:
				continue
			if 'p' in row[0]:
				self.param.update({row[0]: row[1]})
			elif 'b2n' in row[0]:
				self._b2n_func = True
				self._b2n_size = int(row[1])
			else:
				if len(row[1]) != bits:
					raise Exception("Row %s in %s is not length %i" % (row, mappingFile, bits))
				self._data2mapping[row[1]] = row[0]
				self._mapping2data[row[0]] = row[1]

	def getmapping(self, data):
		if self._b2n_func:
			try:
				binc = chunkstring(data, self._b2n_size)
				val = list(map(lambda a: int(a,2), binc))
				#print(data,val)
				if not val:
					return None
				else:				
					return val[0]
			except KeyError:
				return None 
		else:
			try:
				return self._data2mapping[data]
			except KeyError:
				return None # modified to return None when there is no message to be sent (end of message)
				#raise Exception("Data %s not found in mapping %s" % (data, self._filename))

	def getdata(self, mapping):
		if self._b2n_func:
			try:
				bformat = '{:0'+str(self._b2n_size)+'b}'
				val = bformat.format(int(mapping))
				return str(val)
			except KeyError:
				raise Exception("Mapping %s not found in mapping %s" % (mapping, self._filename))
		else:
			try:
				return self._mapping2data[mapping]
			except KeyError:
				raise Exception("Mapping %s not found in mapping %s" % (mapping, self._filename))

	def getparams(self):
		try:
			return self.param
		except KeyError:
			return None
