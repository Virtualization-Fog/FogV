#!/usr/bin/python
# importing the random module
import random

class Task:
	 'Class Structure for Sensor'
	 ' Constructor with zero or multiple parameter'
	 def __init__(self,arrivalTime=0,serviceTime=0,proT=0,inService=0,vmID=-1): #-1 no assigned VM and 0 means this task is not in the service
			self.arrivalTime=arrivalTime
			self.serviceTime=serviceTime
			self.proT=proT
			self.inService=inService
			self.vmID=vmID
			'Function to set sensor information'
	 def __str__(self):
		  return 'Task id {self.id} type{self.type} datatype {self.datatype} data {self.data} '.format(self=self)
	 def setArrivalTime(self,t):
			self.arrivalTime=t

	 def  setServiceTime(self,t):
			self.serviceTime=t
            
	 def  setProTime(self,t):
			self.proT=t       

	 def setinServices(self,status):
			self.inService=status

	 def setVmID(self,ID):
			self.vmID=ID

	 def getArrivalTime(self):
			return self.arrivalTime

	 def getServiceTime(self):
			return self.serviceTime
        
        
	 def getProTime(self):
			return self.proT    

	 def getinServices(self):
			return self.inService

	 def getVmID(self):
			return self.vmID
