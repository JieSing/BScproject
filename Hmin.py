# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:20:35 2021

@author: jsy18
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

def rtheta(theta):
    if theta>np.pi:
        theta-=2*np.pi
        return rtheta(theta)
    if theta<-np.pi:
        theta+=2*np.pi
        return rtheta(theta)
    if theta>-np.pi and theta< np.pi:
        return theta

def H_min(x):
    #calculate H_min, x is the value of the noise
    if rtheta(x)>=0:
        return -np.log2(np.sin((np.pi/2+x)/2)**2)
    else:
        return -np.log2(np.cos((np.pi/2+x)/2)**2)
    
    
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
        self.Hminn=[]
        self.Hminu=[]
        self.Hmind=[]
        self.thetan=[]
        self.thetau=[]
        self.thetad=[]
        
    def reset(self):
        self.theta=0
        self.phi=0
        
    def roty(self):
        rot=np.pi/2
        self.theta+=rot
    
    def noisen(self):
        noise = np.random.normal(0,self.noiseParam)
        self.theta+=noise
        return noise
            
    def noiseu(self):       #uniform distribution 
        width=(self.noiseParam**2*12)**0.5
        noise = np.random.uniform(-width/2,width/2)
        self.theta+=noise
        return noise
        
    def noised(self):
        noise =np.random.choice([-self.noiseParam,self.noiseParam],p=[0.5,0.5])
        self.theta+=noise 
        return noise
        
    def run2(self, rep=8000):
        for i in range(rep):
            self.reset()
            self.roty()
            n=self.noisen()
            self.theta=rtheta(self.theta)
            self.Hminn.append(H_min(n))
            self.reset()
            self.roty()
            n=self.noiseu()
            self.theta=rtheta(self.theta)
            self.Hminu.append(H_min(n))
            self.reset()
            self.roty()
            n=self.noised()
            self.theta=rtheta(self.theta)
            self.Hmind.append(H_min(n))

noiseParamList=np.arange(0.0001,5,0.1)
xdata=[]
meanHminn=[]
meanHminu=[]
meanHmind=[]
meanthetan=[]
meanthetau=[]
meanthetad=[]


for n in noiseParamList:
    a = QR(n)
    a.run2(rep=10000)
    
    meanHminn.append(np.average(a.Hminn))
    meanHminu.append(np.average(a.Hminu))
    meanHmind.append(np.average(a.Hmind))
    xdata.append(n)
    print(n)



fig=plt.figure(2)
plt.plot(xdata,meanHminn,color='r',linestyle='',marker='.',label='Normal Distribution')
plt.plot(xdata,meanHminu,color='b',linestyle='',marker='.',label='Uniform Distribution')
plt.plot(xdata,meanHmind,color='g',linestyle='',marker='.',label='Two Delta Function')
plt.xlabel('noise parameter (sigma)')
plt.ylabel('<H_min>')


def fnormal(n):
    return integrate.quad(lambda x: ((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*H_min(x), 0,10*n)
def funiform(w):
    return integrate.quad(lambda x: (1/w)*H_min(x), -w/2,w/2)
def fdelta(loc):
    return 0.5*H_min(-loc)+0.5*H_min(loc)

xsigma=np.arange(0.0001,5,0.001)
yn=[]
yu=[]
yd=[]
for sigma in xsigma:
    yn.append(fnormal(sigma)[0])
    yu.append(funiform((sigma**2*12)**0.5)[0])
    yd.append(fdelta(sigma))
    
    
    
plt.plot(xsigma,yn,alpha=0.5,label='normal distribution theoretical')
plt.plot(xsigma,yu,alpha=0.5,label='uniform distribution theoretical')
plt.plot(xsigma,yd,alpha=0.5,label='delta distribution theoretical')

plt.title('mean min-entropy')
plt.legend()
plt.show()


