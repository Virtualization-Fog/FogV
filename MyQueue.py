class queue:
	def __init__(self,maxSize=0):
		self.maxSize =maxSize
		self.buffer=[]
		self.sumW = 0;
		self.sumW2 = 0;
		self.sumS = 0;
		self.sumS2 = 0;
		self.n = 0;
		self.surface = 0;
		self.t = 0;
		self.timeCPUBusy=0
		self.timeBlock=0;
		self.surfaceBlock=0;
	def setSize(self,s):
		self.maxSize=s
	def getSize(self):
		return len(self.buffer)

	def add(self,sensor):
		size=len(self.buffer)
		currentTime = sensor.getArrivalTime()
		if currentTime>self.t:
			self.t=currentTime
		
# 		print("currentTime = ",currentTime," t = ",self.t)
		
		self.surface+=(size*(currentTime - self.t))
		
		self.buffer.append(sensor)

	def enterService(self,ID):
		for i in range(len(self.buffer)):
			task=self.buffer[i]
			if task.getinServices()==0 and task.getVmID()==-1:
				task.setinServices(1)
				task.setVmID(ID)
				self.buffer[i]=task
				break 
     
	def dequeue(self):
		s=self.buffer.pop(0)
		return s

	def ClacStatictics(self,currentTime,arrivalTime,serviceTime,proT):
		size = len(self.buffer)
		if currentTime < arrivalTime:
 			print("Negeative 44444444444444444444444444444444",currentTime,"  -  ",arrivalTime)
             
		self.sumS+= (currentTime - arrivalTime)+proT+(0.5*proT)
		self.sumS2+= (currentTime-arrivalTime) * (currentTime - arrivalTime)
# 		
		self.sumW += (currentTime-arrivalTime-serviceTime)
# 		if currentTime-arrivalTime-serviceTime < 0:
#  			print("Negeative 3")

# 		print("currentTime -- ",currentTime," , arrival time ", arrivalTime," , service time", serviceTime)
		self.sumW2+= (currentTime - arrivalTime - serviceTime) * (currentTime - arrivalTime - serviceTime)
		self.n+=1
# 		if self.n%10==0 :
# 			input("Press Enter  :")
		self.timeCPUBusy+=serviceTime
		self.surface += size * (currentTime - self.t)
		self.t=currentTime
        
        
	def ClacStaticticsLocal(self,currentTime,arrivalTime,serviceTime):
		size = len(self.buffer)+1
		if currentTime < arrivalTime:
			print("Negeative 2")
		self.sumS+= currentTime - arrivalTime
		self.sumS2+= (currentTime-arrivalTime) * (currentTime - arrivalTime)
		#print("currentTime-s.getArrivalTime()-s.getServiceTime()",len(self.buffer)," -- ",currentTime," , ", arrivalTime," , ", serviceTime)
		self.sumW += currentTime-arrivalTime-serviceTime
		if (currentTime-arrivalTime-serviceTime) < 0:
			print("Negeative 3")
		self.sumW2+= (currentTime - arrivalTime - serviceTime) * (currentTime - arrivalTime - serviceTime)
		self.n+=1
		self.timeCPUBusy+=serviceTime
		self.surface += size * (currentTime - self.t)
		self.t=currentTime        

	def getSensorAtHead(self,vmID):
		for i in range(len(self.buffer)):
			task=self.buffer[i]
			if task.getinServices()==0 and task.getVmID()==-1:
				task.setinServices(1)
				task.setVmID=vmID
				self.buffer[i]=task
				return task.getServiceTime()

		return -1

	def bufferBlock(self,currentTime):
		self.surfaceBlock+=currentTime

	def getsurfaceBlock(self):
		return self.surfaceBlock
	def getBlock(self,tt):
		return	self.surfaceBlock/tt

	def getMeanWaitingTime(self): # task waiting time in queue
# 		print(" n = ",self.n)
		if self.n==0:
			return 0
		else:
			return self.sumW / self.n
	def getMeanSojournTime(self): # response time
		#print(" n = ",self.n," and self.sumS =  ",self.sumS )
		if self.n==0:
			return 0
		else:
			return self.sumS / self.n
	def getMeanNumberOfSensors(self):
		return self.surface/self.t
	def getUtilization(self):  # CPU utilization
		return self.timeCPUBusy/self.t
	def getThroughput(self,mu): # System throughput
		return (self.timeCPUBusy/self.t)*mu
	def getallSystemTime(self): # System throughput
		return self.sumS
	def getNumOfServiedTasks(self): # System throughput
		return self.n
	def getallQueueingTime(self): # System throughput
		return self.sumW



