class virtualMachine():
    def __init__(self,state=0,t=0,arr=0,ser=0,proT=0):
        self.state = state
        self.departureTime=t
        self.arrivalTime=arr
        self.serviceTime=ser
        self.proT=proT

    def setState(self,state):
        self.state=state

    def getState(self):
        return self.state
    def setDepartureTime(self,departureTime):
        self.departureTime=departureTime

    def getDepartureTime(self):
        return self.departureTime

    def setArrivalTime(self,arri):
        self.arrivalTime=arri
    def getArrivalTime(self):
        return self.arrivalTime

    def setServiceTime(self,serv):
        self.serviceTime=serv
    def getServiceTime(self):
        return self.serviceTime
    
    def setProTime(self,proT):
        self.proT=proT
    def getProTime(self):
        return self.proT    


