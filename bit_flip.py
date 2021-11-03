# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 10:43:31 2021

@author: jsy18
"""

import numpy as np
import matplotlib.pyplot as plt
        
def rng(num,prob):
    return np.random.choice(2, num, p=[1-prob,prob])

class bit_flip_code():
    
    def __init__(self,num=50):
        self.in_qubit1 = np.random.choice(2, num, p=[0.5,0.5])
        self.in_qubit2 = np.array(self.in_qubit1)
        self.in_qubit3 = np.array(self.in_qubit1)
        self.in_qubit_in = np.array(self.in_qubit1)
#        self.

    
    def bit_flip(self,tt=0.2):
        
        x1 = rng(num=len(self.in_qubit1),prob=tt)
        x2 = rng(num=len(self.in_qubit1),prob=tt)
        x3 = rng(num=len(self.in_qubit1),prob=tt)
        
        for i in range(0,len(x1)):
            if x1[i]==1:
                if self.in_qubit1[i]==0:
                    self.in_qubit1[i]=1
                else:
                    self.in_qubit1[i]=0
                    
        for i in range(0,len(x2)):
            if x2[i]==1:
                if self.in_qubit2[i]==0:
                    self.in_qubit2[i]=1
                else:
                    self.in_qubit2[i]=0
            
        for i in range(0,len(x3)):
            if x3[i]==1:
                if self.in_qubit3[i]==0:
                    self.in_qubit3[i]=1
                else:
                    self.in_qubit3[i]=0
                            

    def error_correct(self):
        
        for j in range(0,len(self.in_qubit1)):
            
            if self.in_qubit1[j] != self.in_qubit2[j]:
                
                if self.in_qubit1[j] != self.in_qubit3[j]:
                    self.in_qubit1[j] = self.in_qubit2[j]            
                else:
                    self.in_qubit2[j] = self.in_qubit1[j]
                    
            elif self.in_qubit2[j] != self.in_qubit3[j]:
                self.in_qubit3[j] = self.in_qubit2[j]  
                
                
#    def check(self):
#        
#        list=[]
#        count=0
#        for k in range(0,len(self.in_qubit_in)):
#            if self.in_qubit2[i] != self.in_qubit_in[i]:
#                count+=1
#                
#        list.append(count) 

#%%     
                
a = bit_flip_code(num=1000)
b = bit_flip_code(num=1000)

alist=[]
blist=[]

x = np.arange(0,0.5,0.05)
for i in x:
    a.__init__(num=1000)    
    a.bit_flip(tt=i)
    a.error_correct()
    
    b.__init__(num=1000)  
    b.bit_flip(tt=i)    
                    
    acount=0
    bcount=0
    for k in range(0,len(a.in_qubit_in)):
        if a.in_qubit2[k] != a.in_qubit_in[k]:
            acount+=1
        if b.in_qubit2[k] != b.in_qubit_in[k]:
            bcount+=1
                
    alist.append(acount) 
    blist.append(bcount)
                 
print(alist)

plt.plot(x,alist,marker='.',label='corrected')
plt.plot(x,blist,marker='.',label='wrong')
plt.ylabel('no of wrong qubits')
plt.xlabel('probability of bit flip')
plt.legend()