# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:38:44 2021

@author: jsy18
"""

import numpy as np
import matplotlib.pyplot as plt
from errcorrect_sigma2 import QR,rng, bit_flip_code

#%%
#normal

#noiseParamList=[0.005,0.01,0.02,0.03,0.05,0.1,0.2,0.3,0.4,0.5]
#noiseParamList=[0.1]
noiseParamList=np.arange(0.01,0.5,0.02)
xdata=[]
ydata1=[]
ydata2=[]

for n in noiseParamList:
    qr1 = QR(inp=0,noiseParam=n)
    for i in range(0,10000):
        qr1.QRrun1()
#    b = bit_flip_code(inp=qr1.result1,inptheta=qr1.thetalist1)
#    b.bit_flip(tt=0.2)

    qr2 = QR(inp=qr1.thetalist1,noiseParam=n)
    qr2.QRrun2()
#    print(qr2.result2)
    countup1=0
    countup2=0
    for i in qr1.result1:
        if i==0:
            countup1+=1
    for i in qr2.result2:
        if i==0:
            countup2+=1
    xdata.append(n)
    ydata1.append(100*countup1/len(qr1.result1))
    ydata2.append(100*countup2/len(qr2.result2))
    print(n)

def writetofile(filename='QRerr.1.1e5.txt'):      #save p(k) and k
        myfile=open(filename,'x')                    
        for i in range(0,len(xdata)):
            myfile.write(str(xdata[i]) + " " + str(ydata2[i]) + '\n') #
            print('i',i)
#        print(max(self.deg_dist))    
        myfile.close()  

#writetofile(filename='QRerr.2.1e5.txt')    
    
fig=plt.figure(1)
plt.plot(xdata,ydata1,'x')
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 1 noisy pi/2 r0  otations in y')
plt.show()
fig=plt.figure(2)
plt.plot(xdata,ydata2,'x',linestyle='',marker='.',label='normal')
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 2 noisy pi/2 rotations in y')
plt.show()


#%%
#bitflip

noiseParamList=[0.005,0.01,0.02,0.03,0.05,0.1,0.2,0.3,0.4,0.5]
#noiseParamList=[0.1]
#noiseParamList=np.arange(0.01,0.5,0.02)
xdata=[]
ydata1=[]
ydata2=[]

for n in noiseParamList:
    qr1 = QR(inp=0,noiseParam=n)
    for i in range(0,1000):
        qr1.QRrun1()
        
    b = bit_flip_code(inptheta=qr1.thetalist1)
    b.bit_flip(tt=0.2)

    qr2 = QR(inp=b.inptheta1,noiseParam=n)
    qr2.QRrun2()
#    print(qr2.result2)
    countup1=0
    countup2=0
    for i in qr1.result1:
        if i==0:
            countup1+=1
    for i in qr2.result2:
        if i==0:
            countup2+=1
    xdata.append(n)
    ydata1.append(100*countup1/len(qr1.result1))
    ydata2.append(100*countup2/len(qr2.result2))
    print(n)

def writetofile(filename='QRerr.1.1e5.txt'):      #save p(k) and k
        myfile=open(filename,'x')                    
        for i in range(0,len(xdata)):
            myfile.write(str(xdata[i]) + " " + str(ydata2[i]) + '\n') #
            print('i',i)
#        print(max(self.deg_dist))    
        myfile.close()  

#writetofile(filename='QRerr.2.1e5.txt')    
    
fig=plt.figure(1)
plt.plot(xdata,ydata1,'x')
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 1 noisy pi/2 r0  otations in y')
plt.show()
fig=plt.figure(2)
plt.plot(xdata,ydata2,'x',linestyle='',marker='.',label='normal')
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 2 noisy pi/2 rotations in y')
plt.show()

#qr.QRrun2()   

#
#self.theta += np.pi/2   
#if self.theta>np.pi:
#    self.theta=2*np.pi - self.theta    
#
#print(qr.result1==b.in_qubit1)
#print(qr.result1==b.in_qubit_in)
#print(qr.thetalist1)         
#print(qr.thetalist2)     

#%%
#errcorrection
#noiseParamList=[0.005,0.01,0.02,0.03,0.05,0.1,0.2,0.3,0.4,0.5]
#noiseParamList=[0.1]
noiseParamList=np.arange(0.01,0.5,0.02)
xdata=[]
ydata1_std=[]
ydata2_std=[]
ydata1_bitflip=[]
ydata2_bitflip=[]
ydata1_errcor=[]
ydata2_errcor=[]

for n in noiseParamList:
    qr1 = QR(inp=0,noiseParam=n)
    for i in range(0,8000):
        qr1.QRrun1()
#    print('qr1.thetalist1',qr1.thetalist1)
        
# std procedure      
    qr2_std = QR(inp=qr1.thetalist1,noiseParam=n)
    qr2_std.QRrun2()
    
    countup1_std=0
    countup2_std=0
    for i in qr1.result1:
        if i==0:
            countup1_std+=1
    for i in qr2_std.result2:
        if i==0:
            countup2_std+=1
    xdata.append(n)
    ydata1_std.append(100*countup1_std/len(qr1.result1))
    ydata2_std.append(100*countup2_std/len(qr2_std.result2))

#bit flip
    b = bit_flip_code(inptheta=qr1.thetalist1)
    b.bit_flip(tt=0.3)
    
#    gg1 = b.inptheta1
#    print(gg1)

    
    qr2_bitflip = QR(inp=b.inptheta1,noiseParam=n)
    qr2_bitflip.QRrun2()
    
#    countup1_bitflip=0
    countup2_bitflip=0
#    for i in qr1.result1:
#        if i==0:
#            countup1_bitflip+=1
    for i in qr2_bitflip.result2:
        if i==0:
            countup2_bitflip+=1
#    ydata1_bitflip.append(100*countup1/len(qr1.result1))
    ydata2_bitflip.append(100*countup2_bitflip/len(qr2_bitflip.result2))

#error correction    
    b.error_correct()

    qr2_errcor = QR(inp=b.inptheta1,noiseParam=n)
    qr2_errcor.QRrun2()

    countup1_errcor=0
    countup2_errcor=0
#    for i in qr1.result1:
#        if i==0:
#            countup1_bitflip+=1
    for i in qr2_errcor.result2:
        if i==0:
            countup2_errcor+=1
#    ydata1_errcor.append(100*countup1/len(qr1.result1))
    ydata2_errcor.append(100*countup2_errcor/len(qr2_errcor.result2))

    print(n)

def writetofile(filename='QRstd.1.5e4.txt'):      #save p(k) and k
        myfile=open(filename,'x')                    
        for i in range(0,len(xdata)):
            myfile.write(str(xdata[i]) + " " + str(ydata2_std[i]) + '\n') #
#            print('i',i)
#        print(max(self.deg_dist))    
        myfile.close()  

def writetofile_bitflip(filename='QRbfp.1.5e4.txt'):      #save p(k) and k
        myfile=open(filename,'x')                    
        for i in range(0,len(xdata)):
            myfile.write(str(xdata[i]) + " " + str(ydata2_bitflip[i]) + '\n') #
#            print('i',i)
#        print(max(self.deg_dist))    
        myfile.close()  
        
def writetofile_errcorrect(filename='QRerr.1.5e4.txt'):      #save p(k) and k
        myfile=open(filename,'x')                    
        for i in range(0,len(xdata)):
            myfile.write(str(xdata[i]) + " " + str(ydata2_errcor[i]) + '\n') #
#            print('i',i)
#        print(max(self.deg_dist))    
        myfile.close()          
        
writetofile(filename='QRstd.2.8e4.txt')    
writetofile_bitflip(filename='QRbfp.2.8e4.txt')
writetofile_errcorrect(filename='QRerr.2.8e4.txt')

#%%
plt.figure(2)
plt.plot(xdata,ydata2_std,'x',linestyle='',marker='.',label='normal')
#plt.plot(xdata,ydata2_bitflip,linestyle='',marker='.',label='bit flip')
#plt.plot(xdata,ydata2_errcor,linestyle='',marker='.',label='err cor')
plt.legend()
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
#plt.title('|0> occurrence after 2 noisy pi/2 rotations in y with error correction')
plt.show()

fig,(ax1, ax2)=plt.subplots(2)
#plt.plot(xdata,ydata2_std,'x',linestyle='',marker='.',label='normal')
ax1.plot(xdata,ydata2_bitflip,linestyle='',marker='.',label='bit flip')
ax2.plot(xdata,ydata2_errcor,linestyle='',marker='.',label='err cor')
ax1.legend()
ax2.legend()
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
#plt.title('|0> occurrence after 2 noisy pi/2 rotations in y with error correction')
plt.show()

#fig=plt.figure(2)
#plt.errorbar(xdata,ydata2_std,'x',linestyle='',marker='.',label='normal')
#plt.errorbar(xdata,ydata2_bitflip,'x',linestyle='',marker='.',label='bit flip')
#plt.errorbar(xdata,ydata2_errcor,'x',linestyle='',marker='.',label='err cor')
#plt.legend()
#plt.xlabel('noise parameter')
#plt.ylabel('percentage of |0> state')
#plt.title('|0> occurrence after 2 noisy pi/2 rotations in y with error correction')
#plt.show()
