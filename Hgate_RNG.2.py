# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:20:35 2021

@author: jsy18
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmath

class QR():
    
    def __init__(self,noiseParam=0.02):
        self.state0=np.array([1,0])
        self.state1=np.array([0,1])
        self.theta=0    #0<=theta<=pi
        self.phi=0
        self.noiseParam=noiseParam
        self.result1=[]
        self.result2=[]
        
    def reset(self):
        self.theta=0
        self.phi=0
        
    def roty(self):
        rot=np.pi/2
        self.theta+=rot
        if self.theta>np.pi:
            self.theta=2*np.pi - self.theta
    
    def noise(self):
        noise =np.random.normal(0,self.noiseParam)
        self.theta+=noise
        if self.theta>np.pi:
            self.theta=2*np.pi - self.theta
            
    def measure(self):
        probup=np.cos(self.theta/2)**2
        probdown=np.sin(self.theta/2)**2
        outcome=np.random.choice(2,p=[probup,probdown])
        return outcome
    
    
    def run(self, rep=500000):
        for i in range(rep):
            self.reset()
            self.roty()
            self.noise()
            self.result1.append(self.measure())
            self.roty()
            self.noise()
            self.result2.append(self.measure())
        #print(self.result)
        
#        


noiseParamList=[0.005,0.01,0.02,0.03,0.05,0.1,0.2,0.3,0.5]
xdata=[]
ydata1=[]
ydata2=[]
for n in noiseParamList:
    a = QR(n)
    a.run()
    countup1=0
    countup2=0
    for i in a.result1:
        if i==0:
            countup1+=1
    for i in a.result2:
        if i==0:
            countup2+=1
    xdata.append(n)
    ydata1.append(100*countup1/len(a.result1))
    ydata2.append(100*countup2/len(a.result2))

fig=plt.figure(1)
plt.plot(xdata,ydata1,'x')
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 1 noisy pi/2 rotations in y')
plt.show()
fig=plt.figure(2)
plt.plot(xdata,ydata2,'x')
plt.xlabel('noise parameter')
plt.ylabel('percentage of |0> state')
plt.title('|0> occurrence after 2 noisy pi/2 rotations in y')
plt.show()
#%%
#x = np.linalg.multi_dot([a._H, [[1,0],[0,np.exp(1)]], a._H])
#print(x)
#df = pd.DataFrame([1,2,3,4], [1,2,3,4])   
#color = ['red','blue','green','orange']
#df.plot(kind='bar', y=0, color=color, legend=False, rot=0)


#%%
import numpy as np

p=[]
ta=[]
for i in range(50000):
    theta=np.random.normal(0,0.03)
    if theta<0:
        theta=-theta
    ta.append(theta)
    p.append(np.sin((np.pi/2+theta)/2)**2)
print(np.average(ta))
print(np.average(p))

noiseParam=0.535263630070409
meanNoise=noiseParam*2**0.5/np.pi**0.5
meanProb=np.sin((np.pi/2+meanNoise)/2)**2
print(meanProb)
minS=-np.log2(meanProb)
print(minS)

