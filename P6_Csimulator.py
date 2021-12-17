# For C Virtual Machines
from VMs import virtualMachine
from numpy import random
from MyQueue import queue
from Task import Task
import random as rn


class Simulator:
    def __init__(self,Alpha=0,Lambda=0,mu=0,Taw=0,metric=0,simLength=0,vmNumber=0,populationSize=0, speedFactor=1, propagationTime=[0, 0, 0, 0], serviceTime=[0, 0, 0, 0]):
        self.Lambda =Lambda
        self.Alpha=Alpha
        self.Taw=Taw
        self.simLength=simLength
        self.FES=[]
        self.rFES=[]
        self.lFES=[]
        self.vmNumber=vmNumber
        self.populationSize=populationSize
        self.remoteQueue=queue(1000)
        self.localQueue=[]
        for i in range(self.populationSize):
            self.localQueue.append(queue(1000))
        self.vm=[]
        self.CPU=[]
        self.t=0
        self.speedFactor=speedFactor
        self.metric=metric
        self.mu=mu
        self.propagationTime=propagationTime
        self.serviceTime=serviceTime
        self.counterR=0
        self.responseR=0
        
    #departureTime,srrivalTiime,serviceTime,transmissionTime, State     
    def isVmIdle(self):
        for i in range(self.vmNumber):
            item=self.vm[i]
            if item[4]==0:
                return i,0
        return -1,-1

    def isCPUIdle(self,id):
            cpu=self.CPU[id]
            if cpu.getState()==0:
                return id,0
            return -1,-1

    def setCPUState(self, id, state,t,arrTime,serTime):
        cpu=self.CPU[id]
        cpu.setState(state)
        cpu.setDepartureTime(t)
        cpu.setArrivalTime(arrTime)
        cpu.setServiceTime(serTime)
        self.CPU[id]=cpu
        
 #departureTime,srrivalTiime,serviceTime,transmissionTime, State     
    def idelBusyNumber(self):
        idle=0
        busy=0
        for i in range(self.vmNumber):
            item=self.vm[i]
            if item[4]==0:
                idle=idle+1
            elif  item[4]==1:
                busy=busy+1
        return idle, busy
 #===============================================================   
    def getMinCPUDepartureVms(self):
        x=[]
        for item in  self.CPU:
            if item.getDepartureTime()>0:
                x.append(item.getDepartureTime())
                
        if len(x)>0:
            return min(x)
        else:
            return 0    
 #departureTime,srrivalTiime,serviceTime,transmissionTime, State 
    def getMinDepartureVms(self):
        x=[]
        for item in  self.vm:
            if item[0]>0:
                x.append(item[0])
                
        if len(x)>0:   
            return min(x)
        else:
           return 0
 # #departureTime,srrivalTiime,serviceTime,transmissionTime, State 
 #    def setVmState(self, id,t,arrTime,serTime,proT,state):
 #        self.vm[id]=(t,arrTime,serTime,proT,state)
        

    def start(self):
        #----------------- For local Buffer ---------------------------------
        #departureTime,srrivalTiime,serviceTime,transmissionTime, State
        for i in range(self.vmNumber):
            self.vm.append((0,0,0,0,0))

        for i in range(self.populationSize):
            self.CPU.append(virtualMachine(0,0))

        for i in range(self.populationSize):
            arrivalRate=round(random.exponential(scale=(1/self.Lambda)))
            if arrivalRate==0:
                arrivalRate=1
            # print("arrivalRate = ",arrivalRate)
            self.FES.append(self.t+arrivalRate)   
         
 #------------------------------------------------------------------           
        while self.t<self.simLength:
  #----------------------------------------------------------
            self.t=min(self.FES)
            if self.t<=0:
                print("hgghgkdjfhgdskjfhgkdjfgh")
            value=self.getMinDepartureVms()
            if value!=0:
                self.t=min(self.t,value)

            value1=self.getMinCPUDepartureVms()
            if value1!=0:
                self.t=min(self.t,value1)
                
            if len(self.rFES)>0:
                min2=min(self.rFES)
                self.t=min(self.t,min2[0])    
            
           
#---------------------- For Arrival scheduing and queueing processes ------------------------
            for i in range(len(self.FES)):
                if int(self.FES[i])==self.t:
                    # print(" Current t ",self.t)
                    arrivalRate=round(random.exponential(scale=(1/self.Lambda)))
                    if arrivalRate==0:
                        arrivalRate=1
                    self.FES[i]=int(self.t+arrivalRate)
                    service=random.exponential(scale=(1/self.mu))
                    if service>self.Taw:
                        if self.propagationTime[0]==1:
                            propT =round(rn.uniform(self.propagationTime[2], self.propagationTime[3]))
                        elif self.propagationTime[0]==0 :
                            propT = self.propagationTime[1]
                            
                        if self.serviceTime[0]==0:
                            serT = self.serviceTime[1]
                        elif  self.serviceTime[0]==1:
                            serT =round(rn.uniform(self.serviceTime[2], self.serviceTime[3]))
                        elif self.serviceTime[0]==2:
                            serT=round(service/self.speedFactor)
                            
                            
                        nextInterArrivalTime=round(self.t+propT)
                        self.rFES.append(tuple((nextInterArrivalTime,serT,propT)))
                    elif service<=self.Taw:
                        task=Task(self.t,round(service),0,-1) # 0 : task is not in service , -1 is not associated with any CPU
                        self.localQueue[i].add(task) # Add task to local queue of MD i
                        id,state=self.isCPUIdle(i)  # check CPU i is idle or not
                        if state==0: # if CPU is idle
                            s=self.localQueue[i].dequeue()  # get task from the head of the queue
                            self.setCPUState(i,1,self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime())
                        
                         
            # if count>1 :
                # print(" t ", self.t," count = ",count," countR = ",countR)           
#------------------ handling the remote task arrival -------------------------------------------------------------
            currentList= list(filter(lambda x: x[0]==self.t, self.rFES)) # get all current arrival event to fog
            self.rFES= list(filter(lambda x: x[0]!=self.t, self.rFES))
            for event in currentList: #if there is any next event for fog
                task=Task(event[0],event[1],event[2],0,-1)
                self.remoteQueue.add(task) # Add task to remote queue
                id,state=self.isVmIdle()  # chech id there is any idle VM
                if state==0: # if VM ide
                    s=self.remoteQueue.dequeue()  # get task from the head of the queue
                    self.vm[id]=(self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime(),s.getProTime(),1)
                    
#------------------------------------ For Deparure handling from fog --------------------
           
            for i in range(len(self.vm)):
                  v=self.vm[i] # get VMs from its List one by one
                
                  if v[0]==self.t and v[4]==1: # if VM i is busy and it must switch to idle now
                    
                      self.remoteQueue.ClacStatictics(self.t,v[1],v[2],v[3]) # Collect statistics
                      self.vm[i]=(0,0,0,0,0)
                      if self.remoteQueue.getSize()>0:
                                  id,state=self.isVmIdle()  # chech id there is any idle VM
                                  if state==0: # if VM ide 
                                      s=self.remoteQueue.dequeue()# Delete the first task from remote queue and return it
                                      self.vm[id]=(self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime(),s.getProTime(),1)
                              
#---------------------------------- For depatrure handling at MD ---------------------------
            for i in range(len(self.CPU)):
                 cpu=self.CPU[i] # get VMs from its List one by one
                 if cpu.getDepartureTime()==self.t and cpu.getState()==1: # if VM i is busy and it must switch to idle now
                     #print("yesser")
                     self.localQueue[i].ClacStaticticsLocal(self.t,cpu.getArrivalTime(),cpu.getServiceTime()) # Collect statistics
                     cpu.setState(0)
                     cpu.setDepartureTime(0)
                     cpu.setArrivalTime(0)
                     cpu.setServiceTime(0)
                     self.CPU[i]=cpu

                     if self.localQueue[i].getSize()>0:
                         id,state=self.isCPUIdle(i)
                         if state==0: # if CPU of MD i is idle
                             s=self.localQueue[i].dequeue()    # get task from the head of the queue
                             self.setCPUState(i,1,self.t+s.getServiceTime(),s.getArrivalTime(),s.getServiceTime())
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
            # self.t=self.t+1
#-----------------------------------------------------------------------------------
        if self.metric==1:
            sum=0
            for i in range(self.populationSize):
                sum=sum+self.localQueue[i].getMeanWaitingTime()
            res1=sum/self.populationSize
            res2 = self.remoteQueue.getMeanWaitingTime()
            res3 = (self.Alpha*res1)+((1-self.Alpha)*res2)
            return (res1,res2,res3)
        elif self.metric==2:
            sum=0
            for i in range(self.populationSize):
                sum=sum+self.localQueue[i].getMeanSojournTime()
            res1=sum/self.populationSize
            res2=self.remoteQueue.getMeanSojournTime()
            res3 = (self.Alpha*res1)+((1-self.Alpha)*res2)
            return (res1,res2,res3)

