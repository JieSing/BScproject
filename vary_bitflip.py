# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 16:35:51 2021

@author: jsy18
"""

# vary the probability of flipping the bit

import numpy as np
import matplotlib.pyplot as plt
from errcorrect_sigma2 import QR,rng, bit_flip_code
import scipy as sp
from scipy.optimize import curve_fit

#%%

#noiseParamList=[0.005,0.01,0.02,0.03,0.05,0.1,0.2,0.3,0.4,0.5]
noiseParamList=[0.3]
#noiseParamList=np.arange(0.01,0.5,0.02)

flipparamlist=np.arange(0.01,0.5,0.02)
xdata=[]
ydata1_std=[]
ydata2_std=[]
ydata1_bitflip=[]
ydata2_bitflip=[]
ydata1_errcor=[]
ydata2_errcor=[]

iteration = 100000
for n in noiseParamList:
    for tprob in flipparamlist:
        qr1 = QR(inp=0,noiseParam=n)
        for i in range(0,iteration):
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
        xdata.append(tprob)
        ydata1_std.append(100*countup1_std/len(qr1.result1))
        ydata2_std.append(100*countup2_std/len(qr2_std.result2))
    
    #bit flip
        b = bit_flip_code(inptheta=qr1.thetalist1)
        b.bit_flip(tt=tprob)
        
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
        print(tprob)

def writetofile_errcorrect(filename='QRerr.1.1e5.txt'):      #save p(k) and k
        myfile=open(filename,'x')                    
        for i in range(0,len(xdata)):
            myfile.write(str(xdata[i]) + " " + str(ydata2_errcor[i]) + '\n') #
            print('i',i)
#        print(max(self.deg_dist))    
        myfile.close()  

#writetofile(filename='QRerr.2.1e5.txt')    


#%%
        
xplist = np.arange(0,0.5,0.01)

def linear(m,x,c):
    return m * x + c

def no_2or3(plist):
    return (3*(plist**2)*(1-plist)+plist**3)*100

popt,pcov = sp.optimize.curve_fit(linear,xdata, ydata2_bitflip)



plt.figure(2)
#plt.plot(xdata,ydata2_std,'x',linestyle='',marker='.',label='normal')
plt.plot(xdata,ydata2_bitflip,linestyle='',marker='.',label='bit flip')
plt.plot(xdata,ydata2_errcor,linestyle='',marker='.',label='err cor')
plt.plot(xplist,linear(popt[0],xplist,popt[1]),linestyle=':',label='Theoretical Prediction')
plt.plot(xplist, no_2or3(xplist),linestyle=':',label='Theoretical Prediction')
plt.legend()
plt.xlabel('Bit Flip parameter')
plt.ylabel('percentage of |0> state')
#plt.title('|0> occurrence after 2 noisy pi/2 rotations in y with error correction')
plt.show()

fig,(ax1, ax2)=plt.subplots(2)
#plt.plot(xdata,ydata2_std,'x',linestyle='',marker='.',label='normal')
ax1.plot(xdata,ydata2_bitflip,linestyle='',marker='.',label='bit flip')
ax2.plot(xdata,ydata2_errcor,linestyle='',marker='.',label='err cor')
ax1.legend()
ax2.legend()
plt.xlabel('Bit Flip parameter')
plt.ylabel('percentage of |0> state')
#plt.title('|0> occurrence after 2 noisy pi/2 rotations in y with error correction')
plt.show()