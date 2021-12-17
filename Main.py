# -------------------------------------------------------------------------------------------------------------------------------------------------
#                                                      *** Code Simulating Mobile-fog IoT System ****
# -------------------------------------------------------------------------------------------------------------------------------------------------
# Title        | Characterization of task response time in fog enabled networks using queueing theory under different virtualization conditions.
# -------------------------------------------------------------------------------------------------------------------------------------------------
# Authors      | Ismail Mohamed, Hassan Al-Mahdi, Mohamed Tahoun, Hamed Nassar.
# -------------------------------------------------------------------------------------------------------------------------------------------------
# Organization | Department of Computer Science, Suez Canal University.
# -------------------------------------------------------------------------------------------------------------------------------------------------
# Address      | Ismailia 41522, Egypt
# ------------------------------------------------------------------------------------------------------------------------------------------------
# E-mails      | {ismail.muhammed, drhassanwwesf, tahoun, nassar}@ci.suez.edu.eg
# ------------------------------------------------------------------------------------------------------------------------------------------------

from P6_Csimulator import Simulator
from datetime import datetime
import math

#print("----------------- Adjust your parameters from corresponding mathematics files -----------------------------")
Lambda = 0.00001      # Task Arrival rate 
speedFactor = 19      # K
C = 5                 # VMs 
N = 500               # TDs
mu = 1/900 	          # Data size distribution
Taw = 900	          # Truncation paramete Tau

#------------------------ Simulation time ----------------------
simlen = 3000000
step   = 0.00003     # Increasing step
#----------------------------------------------------------------
metric = 2  # Sojourn Time for local processing
#----------------------------------------------------------------
propagationTime = [0, 20, 10, 100]    # First Para = 0 -> Perfect deterministic
serviceTime     = [2, 40, 30, 100]    # First Para = 0 -> Perfect deterministic, 1-> Semi-Perfect uniform (a,b) third and foruth items
                                      # First para = 2---> For Baseline
#-------------------------------------------------------------------
e        = math.exp(-mu*Taw) 			# e = e^(-mu*Taw)
Alpha    = 1 - e
Lambda_R = N*Lambda*(1-Alpha)
print("Alpha = ", Alpha, sep='')
#-------------------------------------------------------------------
if serviceTime[0]==0:
    E_servT=serviceTime[1]
elif serviceTime[0]==1:
    E_servT= (serviceTime[2]+serviceTime[3])/2
else:
    E_servT=  ((Taw*mu) + 1)/(speedFactor*mu) 
    
muF  = 1/(E_servT)
#----------------------------------------------------------------
localOut  = open("Sim_localresult_L3.txt", "w")
remoteOut = open("Sim_remoteresult_L3.txt", "w")
wieghtOut = open("Sim_Overall_L3.txt", "w")

response1 = []
response2 = []
response3 = []

choice = input('''Choose the varying parameter of the experiment: 
               1. The number of VMs (C).
               2. The off-loading thresohld (Taw).
               3. The number of terminal devices (N).
               4. The arrival rate of processes (Lambda).
               Your Choice is ''')
print('Simulation Started at', datetime.now().strftime("%H:%M:%S"))

#------------------------- For varing C ------------------------------
if choice=='1':
    print("N (MDs) = ", N, ", Taw = ", Taw, ", Speed = ", speedFactor, ", Lambda = ",
          Lambda,", mu = ", mu, ", Alpha = ", Alpha)
    C      = 2
    Lambda = 0.0001
    e      = math.exp(-mu*Taw) 			# e = e^(-mu*Taw)
    Alpha  = (1 - e)
    Lambda_R = N*Lambda*(1-Alpha)
    while C<=30:
        Stability = C/E_servT 
        if Lambda_R >= Stability:
              print("Stability>>>")
              break;
        sim = Simulator(Alpha, Lambda, mu, Taw, metric, simlen, C, N, speedFactor, propagationTime, serviceTime)
        (result1, result2, result3) = sim.start()
        print("(", C, ", ", result1, ", ", result2, ", ", result3, ")", sep='')
        localOut.write("(" +repr(C)+", "+repr(result1)+")"+"\n")
        remoteOut.write("("+repr(C)+", "+repr(result2)+")"+"\n")
        wieghtOut.write("("+repr(C)+", "+repr(result3)+")"+"\n")
        C+=2

#--------------------------- For Varing taw  -------------------------
if choice=='2':
    Lambda=0.0001
    print("N (MDs) = ",N," C (VMs) = ",C,"Speed = ",speedFactor,"Lambda = ",Lambda," mu = ",mu)
    Taw=200
    while Taw<=2000:
        e=math.exp(-mu*Taw) 			# e = e^(-mu*Taw)
        Alpha=(1 - e)
        Lambda_R = N*Lambda*(1-Alpha) 
        Stability=C/E_servT 
        if Lambda_R >=Stability:
            print("Out of Stability")
            break;
        sim=Simulator(Alpha,Lambda ,mu,Taw,metric,simlen,C,N,speedFactor, propagationTime, serviceTime)
        (result1,result2,result3)=sim.start()
        print("(", Taw, ", ", result1, ", ", result2, ", ", result3, ")", sep='')
        localOut.write("(" +repr(Taw)+", "+repr(result1)+")"+"\n")
        remoteOut.write("("+repr(Taw)+", "+repr(result2)+")"+"\n")
        wieghtOut.write("("+repr(Taw)+", "+repr(result3)+")"+"\n")
        Taw+=200

#-------------------------- For varing N -----------------------------
elif choice=='3':
    print("N (MDs) = ", N, ", C (VMs) = ", C, ", Speed = ", speedFactor, ", Lambda = ", Lambda, ", mu = ", mu, ", Alpha = ", Alpha, sep='')
    Stability=C/E_servT 
    print("Taw ",Taw," C (VMs) = ",C,"Speed = ",speedFactor,"Lambda = ",Lambda," mu = ",mu," Alpha = ",Alpha)
    N=200
    Lambda=0.00001
    Lambda_R = N*Lambda*(1-Alpha)  
    while N<=1800:
        if Lambda_R>=Stability:
            print("Out of Stability")
            break;
        sim=Simulator(Alpha,Lambda,mu,Taw,metric,simlen,C,N,speedFactor, propagationTime, serviceTime)
        (result1,result2,result3)=sim.start()
        print("(",N,", ",result1,", ",result2,", ",result3,")", sep='')
        localOut.write("(" +repr(N)+", "+repr(result1)+")"+"\n")
        remoteOut.write("("+repr(N)+", "+repr(result2)+")"+"\n")
        wieghtOut.write("("+repr(N)+", "+repr(result3)+")"+"\n")
        N+=200
        Lambda_R = N*Lambda*(1-Alpha)  

#---------------------- For Varing Lambda -----------------------------
elif choice=='4':
    print("N (MDs) = ", N, ", C (VMs) = ", C, ", Speed = ", speedFactor, ", Lambda = ", Lambda, ", mu = ", mu, ", Alpha =", Alpha, sep='')
    
    Stability = C/E_servT 
  
    while Lambda_R< Stability:
    # while Lambda <= 0.00025:
        # print("Lambda_R = ",Lambda_R)
        sim=Simulator(Alpha,Lambda,mu,Taw,metric,simlen,C,N,speedFactor, propagationTime, serviceTime)
        (result1,result2,result3)=sim.start()
        print("(",Lambda,", ",result1,", ",result2,", ",result3,")", sep='')
        localOut.write("(" +repr(Lambda)+", "+repr(result1)+")"+"\n")
        remoteOut.write("("+repr(Lambda)+", "+repr(result2)+")"+"\n")
        wieghtOut.write("("+repr(Lambda)+", "+repr(result3)+")"+"\n")
        Lambda+=step
        Lambda_R = N*Lambda*(1-Alpha) 

#---------------------- For Varing Lambda -----------------------------
      
localOut.close()
remoteOut.close()
wieghtOut.close()       
#----------------------------------------------------------------------------
print('Simulation Ended at', datetime.now().strftime("%H:%M:%S"))
