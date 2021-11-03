# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:20:35 2021

@author: jsy18
"""
import numpy as np
import matplotlib.pyplot as plt

class QR():
    
    def __init__(self,noiseParam=0.02):
        self.state0=np.array([1,0])
        self.state1=np.array([0,1])
        self.theta=0    #0<=theta<=pi
        self.phi=0
        self.noiseParam=noiseParam
        self.result1n=[]
        self.result2n=[]
        self.result1u=[]
        self.result2u=[]
        self.result1d=[]
        self.result2d=[]
        
    def reset(self):
        self.theta=0
        self.phi=0
        
    def roty(self):
        rot=np.pi/2
        self.theta+=rot
    
    def noisen(self):
        noise = np.random.normal(0,self.noiseParam)
        self.theta+=noise
            
    def noiseu(self):       #uniform distribution 
        width=(self.noiseParam**2*12)**0.5
        noise = np.random.uniform(-width/2,width/2)
        self.theta+=noise
        
    def noised(self):
        noise =np.random.choice([-self.noiseParam,self.noiseParam],p=[0.5,0.5])
        self.theta+=noise
            
#    def noise_poisson(self):
#        np.random.random
            
    def measure(self):
        probup=np.cos(self.theta/2)**2
        probdown=np.sin(self.theta/2)**2
        outcome=np.random.choice(2,p=[probup,probdown])
        return outcome
    
    
    def run(self, rep=70000):
        for i in range(rep):
            self.reset()
            self.roty()
            self.noisen()
            self.result1n.append(self.measure())
            self.roty()
            self.noisen()
            self.result2n.append(self.measure())
            self.reset()
            self.roty()
            self.noiseu()
            self.result1u.append(self.measure())
            self.roty()
            self.noiseu()
            self.result2u.append(self.measure())
            self.reset()
            self.roty()
            self.noised()
            self.result1d.append(self.measure())
            self.roty()
            self.noised()
            self.result2d.append(self.measure())
        #print(self.result)
        
#        


noiseParamList=[0.005,0.01,0.02,0.03,0.05,0.1,0.2,0.3,0.5]
xdata=[]
ydata1n=[]
ydata2n=[]
ydata1u=[]
ydata2u=[]
ydata1d=[]
ydata2d=[]
for n in noiseParamList:
    a = QR(n)
    a.run()
    countup1n=0
    countup2n=0
    countup1u=0
    countup2u=0
    countup1d=0
    countup2d=0
    for i in a.result1n:
        if i==0:
            countup1n+=1
    for i in a.result2n:
        if i==0:
            countup2n+=1
    for i in a.result1u:
        if i==0:
            countup1u+=1
    for i in a.result2u:
        if i==0:
            countup2u+=1
    for i in a.result1d:
        if i==0:
            countup1d+=1
    for i in a.result2d:
        if i==0:
            countup2d+=1
    xdata.append(n)
    ydata1n.append(100*countup1n/len(a.result1n))
    ydata2n.append(100*countup2n/len(a.result2n))
    ydata1u.append(100*countup1u/len(a.result1u))
    ydata2u.append(100*countup2u/len(a.result2u))
    ydata1d.append(100*countup1d/len(a.result1d))
    ydata2d.append(100*countup2d/len(a.result2d))

fig=plt.figure(1)
plt.plot(xdata,ydata1n,'x',label='Normal Distribution')
plt.plot(xdata,ydata1u,'x',label='Uniform Distribution')
plt.plot(xdata,ydata1d,'x',label='Two Delta Function')
plt.xlabel('noise parameter (sigma)')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 1 noisy pi/2 rotations in y')
plt.legend()
plt.show()
xd=np.arange(0,0.5,0.01)
yd=[]
for x in xd:
    yd.append(50*x**2)
fig=plt.figure(2)
plt.plot(xdata,ydata2n,'x',label='Normal Distribution')
plt.plot(xdata,ydata2u,'x',label='Uniform Distribution')
plt.plot(xdata,ydata2d,'x',label='Two Delta Function')
plt.plot(xd,yd,label='y=0.5*sigma**2')
plt.xlabel('noise parameter (sigma)')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 2 noisy pi/2 rotations in y')
plt.legend
plt.show()

#%%

from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np

p=[]
ta=[]
for i in range(50000):
    theta=np.random.normal(0,0.03)
    if theta<0:
        theta=-theta
    ta.append(theta)
    p.append(np.sin((np.pi/2+theta)/2)**2)
#print(np.average(ta))
#print(np.average(p))

noiseParam=1.0
meanNoise=noiseParam*2**0.5/np.pi**0.5
meanProb=np.sin((np.pi/2+meanNoise)/2)**2

minS=-np.log2(meanProb)
print('Standard deviation = %s'%(noiseParam))
print('S_min(P_max(<delta>))')
print(minS)
result=integrate.quad(lambda x :((2/np.pi)**0.5*np.e**(-x**2/(2*noiseParam**2))/noiseParam)*-np.log2(np.sin((np.pi/2+x)/2)**2),0,np.inf)
print('<S_min(P_max(delta))>')
print(result[0])

def func(n):
    return integrate.quad(lambda x :((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*-np.log2(np.sin((np.pi/2+x)/2)**2),0,np.pi)[0]+integrate.quad(lambda x :((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*-np.log2(np.cos((np.pi/2+x)/2)**2),np.pi,2*np.pi)[0]+integrate.quad(lambda x :((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*-np.log2(np.sin((np.pi/2+x)/2)**2),2*np.pi,3*np.pi)[0]+integrate.quad(lambda x :((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*-np.log2(np.cos((np.pi/2+x)/2)**2),3*np.pi,4*np.pi)[0]+integrate.quad(lambda x :((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*-np.log2(np.sin((np.pi/2+x)/2)**2),4*np.pi,5*np.pi)[0]
x=np.arange(0.001,np.pi,0.001)
y=[]
for i in x:
    y.append(func(i)) 

plt.plot(x,y)
plt.xlabel('sigma')
plt.ylabel('<H_min>')
plt.show()



