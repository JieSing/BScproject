# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 21:56:37 2021

@author: ZZ
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import integrate

class QR():
    
    def __init__(self,noiseParam=0.02):
        self.state0=np.array([1,0])
        self.state1=np.array([0,1])
        self.theta=0    #0<=theta<=pi
        self.phi=0
        self.noiseParam=noiseParam
        
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
    
        
    def runNormal1(self):
        self.reset()
        self.roty()
        noise=self.noisen()
        return noise,self.measure()
    
    def runNormal2(self):
        self.reset()
        self.roty()
        self.noisen()
        self.roty()
        self.noisen()
        return self.measure()
    
    
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
    
def fnormal(n):
    #function that calculates <H_min> based on a given noise parameter
    return integrate.quad(lambda x: ((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*H_min(x), 0,10*n)

class guesser():
    def __init__(self,RNG):
        self.RNG=RNG
        self.est_std=0
        self.correctGuess=0
        self.totalGuess=0
        self.result=[0,0]
        
    def estimate(self,rep):
        #used in correction 
        for i in range(rep):
            retVal=self.RNG.runNormal2()
            if retVal==0:
                self.result[0]+=1
                self.result[1]+=1
            else:
                self.result[1]+=1
        return np.sqrt(self.result[0]*2/self.result[1])
    
    def correction(self,inirep=2000):
        #trying to estimate the noise parameter
        self.est_std=self.estimate(inirep)
        temp=self.estimate(50)
        while(np.absolute(self.est_std-temp)>0.00001):
            self.est_std=temp
            temp=self.estimate(500)
        self.est_std=temp
        print('Estimated STD is %s'%(self.est_std))
        print('Average H_min using estimated STD: %s'%(fnormal(self.est_std)[0]))
        
    
    def guess(self, rep=5000):
        #the guesser that knows the value of each noise
        sumHmin=0
        for i in range(rep):
            noise,outcome=self.RNG.runNormal1()
            sumHmin+=H_min(noise)
            guess=-1
            if rtheta(noise)>0:
                guess=1
            elif rtheta(noise)<0:
                guess=0
            else:
                guess=np.random.choice(2,p=[0.5,0.5])
            if guess==outcome:
                self.correctGuess+=1
                self.totalGuess+=1
            else:
                self.totalGuess+=1
        #print('Number of correct guesses %s'%(self.correctGuess))
        #print('Total guesses %s'%(self.totalGuess))
        print('Probability of the guesser guessing correctly is %s percent'%(self.correctGuess*100/self.totalGuess))
        print('True total H_min for %s bits generated: %s'%(rep,sumHmin))
        
    
truestd=random.random()/2
rep=50000
print('Actual STD is set to %s'%(truestd))
print('Average H_min using true STD = %s'%(fnormal(truestd)[0]))
print('which corresponds to a probability of guessing correctly on average p=%s'%(100*2**(-fnormal(truestd)[0])))
RNG=QR(truestd)
g=guesser(RNG)
g.correction()
g.guess(rep)
print('Total H_min using average H_min of true STD: %s'%(fnormal(truestd)[0]*rep))
print('Estimated total H_min using average H_min of estimated STD: %s'%(fnormal(g.est_std)[0]*rep))