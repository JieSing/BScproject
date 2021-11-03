# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 12:50:53 2021

@author: jsy18
"""

import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

class QR():
    
    def __init__(self,noiseParam=0.02,inp=0):
        self.state0=np.array([1,0])
        self.state1=np.array([0,1])
        self.theta=0    #0<=theta<=pi
        self.phi=0
        self.noiseParam=noiseParam
        self.result1=[]
        self.result2=[]
        self.thetalist1 = []
        self.thetalist2 = []
        self.inptheta = deepcopy(inp)
        
    def reset(self):
        self.theta=0
        self.phi=0
        
    def roty(self):
        rot=np.pi/2
        self.theta+=rot
#        if self.theta>np.pi:
#            self.theta=2*np.pi - self.theta
    
    def noise(self):
        noise = np.random.normal(0,self.noiseParam)
        self.theta+=noise
#        if self.theta>np.pi:
#            self.theta=2*np.pi - self.theta
            
    def noise2(self,k):
        noise2 = np.random.normal(0,self.noiseParam)
#        print('self.inptheta1',self.inptheta)
        self.inptheta[k]+=noise2
#        if self.inptheta[k]>np.pi:
#            self.inptheta[k]=2*np.pi - self.inptheta[k]
 
            
    def noise_flat(self):       #uniform distribution 
        noise = np.random.uniform(-self.noiseParam,self.noiseParam)
        self.theta+=noise
#        if self.theta>np.pi:
#            self.theta=2*np.pi - self.theta
            
#    def noise_poisson(self):
#        np.random.random
                               
    def measure(self):
        probup=np.cos(self.theta/2)**2
        probdown=np.sin(self.theta/2)**2
        outcome=np.random.choice(2,p=[probup,probdown])
        return outcome
    
    def measure2(self,k):
        probup=np.cos(self.inptheta[k]/2)**2
        probdown=np.sin(self.inptheta[k]/2)**2
        outcome=np.random.choice(2,p=[probup,probdown])
#        self.inptheta
#        print('prob',probup,probdown)
        return outcome
    
    
    def QRrun1(self):
        self.reset()
        self.roty()
        self.noise()
        self.thetalist1.append(self.theta)
        self.result1.append(self.measure())
    
    def QRrun2(self):
        rot=np.pi/2
        for i in range(0,len(self.inptheta)):
            self.inptheta[i] +=rot
#            if self.inptheta[i]>np.pi:
#                self.inptheta[i]=2*np.pi - self.inptheta[i]
            self.noise2(k=i)
            self.result2.append(self.measure2(k=i))
#        print('self.thetalist2',self.thetalist2)  
#        print('self.inptheta2',self.inptheta)
        self.thetalist2 = self.inptheta
#        print('self.thetalist2',self.thetalist2)
        #print(self.result)

        
def rng(num,prob):
    return np.random.choice(2, num, p=[1-prob,prob])

class bit_flip_code():
    
    def __init__(self,inptheta=[1,2,3]):
#        self.in_qubit1 = np.array(inp)
#        self.in_qubit2 = np.array(self.in_qubit1)
#        self.in_qubit3 = np.array(self.in_qubit1)
#        self.in_qubit_in = np.array(self.in_qubit1)
        self.state0=np.array([1,0])
        self.state1=np.array([0,1])
        self.inptheta1 = deepcopy(inptheta)
        self.inptheta2 = deepcopy(inptheta)
        self.inptheta3 = deepcopy(inptheta)
        
    
    def bit_flip(self,tt=0.2):
        
        x1 = rng(num=len(self.inptheta1),prob=tt)
        x2 = rng(num=len(self.inptheta2),prob=tt)
        x3 = rng(num=len(self.inptheta3),prob=tt)
#        print('init',self.inptheta1)
        
        for i in range(0,len(x1)):
            if x1[i]==1:
                self.inptheta1[i] += np.pi
#                print(i)
#                print('correcting1',self.inptheta1)
                                                
        for i in range(0,len(x2)):
            if x2[i]==1:
                self.inptheta2[i] += np.pi
#                print(i)
#                print('correcting2',self.inptheta2)
            
        for i in range(0,len(x3)):
            if x3[i]==1:
                self.inptheta3[i] += np.pi
#                print(i)
#                print('correcting3',self.inptheta3)
                
#        print('checkx1',x1 == x2)
#        print(x1)       
#        print('final',self.inptheta1)
#        print(self.inptheta1 == inptheta)
        print('check1',self.inptheta1 == self.inptheta2)
                    
#    def bitflip_normal(self):
        
                            

    def error_correct(self):
        
        for j in range(0,len(self.inptheta1)):
            
            if self.inptheta1[j] != self.inptheta2[j]:
                
                if self.inptheta1[j] != self.inptheta3[j]:
                    self.inptheta1[j] = self.inptheta2[j]            
                else:
                    self.inptheta2[j] = self.inptheta1[j]
                    
            elif self.inptheta2[j] != self.inptheta3[j]:
                self.inptheta3[j] = self.inptheta2[j]  
             
        print('check2',self.inptheta1 == self.inptheta2)




