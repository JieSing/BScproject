# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 08:32:42 2021

@author: ZZ
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

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
    if rtheta(x)>=0:
        return -np.log2(np.sin((np.pi/2+x)/2)**2)
    else:
        return -np.log2(np.cos((np.pi/2+x)/2)**2)
    

    
    
def fnormal(n):
    return integrate.quad(lambda x: ((2/np.pi)**0.5*np.e**(-x**2/(2*n**2))/n)*H_min(x), 0,10*n)
def funiform(w):
    return integrate.quad(lambda x: (1/w)*H_min(x), -w/2,w/2)
def fdelta(loc):
    return 0.5*H_min(-loc)+0.5*H_min(loc)

xsigma=np.arange(0.00001,0.5,0.01)
yn=[]
yu=[]
yd=[]
for sigma in xsigma:
    yn.append(fnormal(sigma)[0])
    yu.append(funiform((sigma**2*12)**0.5)[0])
    yd.append(fdelta(sigma))
    
    
    
plt.plot(xsigma,yn,alpha=0.5,label='normal distribution')
plt.plot(xsigma,yu,alpha=0.5,label='uniform distribution')
plt.plot(xsigma,yd,alpha=0.5,label='delta distribution')
plt.xlabel('sigma')
plt.ylabel('<H_min>')
plt.title('mean min-entropy')
plt.legend()
plt.show()

#%%
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

x=np.arange(0.0001,0.5,0.01)
yn=[]
yu=[]
yd=[]
for s in x:    
    output=integrate.dblquad(lambda y,x:(1/(s*(2*np.pi)**0.5) *np.e**(-x**2/(2*s**2)))*(1/(s*(2*np.pi)**0.5) *np.e**(-y**2/(2*s**2)))*np.cos((np.pi+x+y)/2)**2 , -5*s,5*s,lambda x: -5*s,lambda x: 5*s)
    yn.append(output[0])
    width=(s**2*12)**0.5
    output=integrate.dblquad(lambda y,x:(1/width)*(1/width)*np.cos((np.pi+x+y)/2)**2 , -0.5*width,0.5*width,lambda x: -0.5*width,lambda x: 0.5*width)
    yu.append(output[0])
    
def f1(x):
    return 0.5*x**2

plt.plot(x,yn,'x',label='Normal distribution')
plt.plot(x,yu,'x',label='Uniform distribution')
plt.plot(x,f1(x),label='0.5*sigma**2')
plt.legend()
plt.show()







    