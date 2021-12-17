class Event():
		"""docstring for ClassName"""
		def __init__(self,e_type='None',time=0,bufferType='None',vmID=0):

			 self.type=e_type
			 self.time=time
			 self.bufferType=bufferType
			 self.vmID=vmID


		def __str__(self):
			 return ' Event type is {self.type} and time = {self.time} '.format(self=self)
		def setTime(self,t):
					self.time=t

		def setType(self,t):
					self.type=t
		def setBufferType(self,bufferType):
					self.bufferType=bufferType
		def getTime(self):
				return self.time
		def getType(self):
				return self.type
		def getBufferType(self):
				return self.bufferType
		def setVmID(self,id):
					self.vmID=id
		def getVmID(self):
					return (self.vmID)

