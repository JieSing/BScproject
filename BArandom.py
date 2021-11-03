# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 11:54:04 2021

@author: jsy18
"""

import numpy as np
#import scipy as sp
#from scipy.optimize import curve_fit
from collections import Counter
import matplotlib.pyplot as plt
from logbin2020 import logbin
from random import sample 
import timeit 
#import random

#undirected graph
#add 1 new vertex
# add m edges
#until reach final number of N vertices
#errorbar

class BArand():
    
    def __init__(self):
        self.graph = {0: [1,2, 3], 1: [0,2,3], 2: [0,1,3], 3: [0,1,2]}#4:[0,2,3], 5:[0,2,3,4]}          #dictionary list
#        self.values = sum(self.graph.values(), [])   
#        self.values = []                            
        self.vertex = list(self.graph.keys())
        self.pref_att_list = np.array([])
        self.t = 0
        
   
#    def getvalues(self):
#        for i in range(0,len(self.graph)):
#            self.values.extend(self.graph[i])
#            print('self.valuesinit',self.values)

                    
    def add(self):        
#        self.t += 1        
        self.graph[len(self.graph)] = []
    
    def connect(self,m=1):      #create an initial graph with N> m
        
        rnd_edge = np.random.choice(self.vertex,replace=False,size=m)
        
        self.vertex.append(len(self.graph)-1)
             
        for eg in range(0, len(rnd_edge)):            
            self.graph[len(self.graph)-1].append(rnd_edge[eg])
            self.graph[rnd_edge[eg]].append(len(self.graph)-1)   
        
#        self.values.extend(list(rnd_edge))
#        
#        for i in range(0,m):
#            self.values.append(len(self.graph)-1)
            
#        print('rnd_edge',rnd_edge)
#        print('self.graph',self.graph)
            
    def connect2(self,m=3):
        
        self.m=m
        #choose a random attachment from a list of all connected nodes with repeated nodes
        rnd_edge = sample(self.vertex,k=m)

            
##        print('self.rnd_edge1',rnd_edge)
        self.rnd_edge = list(set(rnd_edge))
#        print('self.rnd_edge2',self.rnd_edge)
#        while len(self.rnd_edge)<m:
#            add_rnd = sample(self.values,k=m-len(self.rnd_edge))
##            print('add_rnd',add_rnd)
#            self.rnd_edge.extend(add_rnd)
##            print('self.rnd_edge3.1',self.rnd_edge)
#            self.rnd_edge = list(set(self.rnd_edge))
#            print('self.rnd_edge3',self.rnd_edge)
            
#        print('m',m)s
#        print(self.vertex)


        self.vertex.append(len(self.graph)-1)
                
#        print('self.rnd_edge',self.rnd_edge)
#        
        for eg in range(0, len(self.rnd_edge)):
            
            self.graph[len(self.graph)-1].append(self.rnd_edge[eg])
            self.graph[self.rnd_edge[eg]].append(len(self.graph)-1)
        
#        self.values.extend(self.rnd_edge)
#        print('self.values2',self.values)
        
#        for i in range(0,m):
#            self.values.append(len(self.graph)-1)
#            print('len(self.graph)',len(self.graph))
#        self.values = sum(self.graph.values(), [])   
#        print('self.values',self.values)  

     
    def run(self, N=1,con=3):
#        con1 = 2*con + 1
        con2 = con + 1         #starts from m+1 nodes
        self.N = N
#        self.getvalues()
        if len(self.graph) <= con2:
            for i in range(0,con2-len(self.graph)+1):
                self.add()
                self.connect(m=len(self.graph)-1)
#                print('self.graph',self.graph)

#        iterate = N-len(self.vertex) 
        for i in range(0,N):            
            self.add()
            self.connect2(m=con)
            print(i/N)    #'fracdone'

            
            
    def total_edge(self):
        self.edge = int(0.5 * len(sum(self.graph.values(), [])))
        return self.edge
        
    
    
    def deg_dist(self):       #calc degree distribution
#        sort_deg = sorted(list(self.graph.values()), key=len)
#        deg_count = 0
        self.val = list(self.graph.values())        #connected edges
        self.deglist = []
        for i in range(0,len(self.val)):
            self.deglist.append(len(self.val[i]))
        self.deg_dist = Counter(self.deglist)
        print(self.deg_dist)    
        
        k = np.arange(min(self.deg_dist),max(self.deg_dist))
        p_k = 2*self.m*(self.m+1)/(k*(k+1)*(k+2))
#        print('p_k',p_k)
        
        plt.figure(2)
        plt.bar(self.deg_dist.keys(),self.deg_dist.values(),label='data')
        plt.plot(k, p_k*self.N,color='orange',label='theory')
        plt.legend()
        plt.ylabel('frequency')
        plt.xlabel('degree k')
        
        from sklearn.metrics import r2_score

        x_k = sorted(self.deg_dist.keys())
        x_k = np.array(x_k)
        p_xk = 2*self.m*(self.m+1)/(x_k*(x_k+1)*(x_k+2))
        
        deg_distvalues = []
        for i in range(1,len(self.deg_dist)+1):
            deg_distvalues.append(self.deg_dist[i])
            
        print(deg_distvalues,len(deg_distvalues))
        print('p_xk',p_xk)
        print(r2_score(deg_distvalues,p_xk*self.N))
        
#        self.degarray = np.array(self.deglist)
#        x_k = 1/(self.degarray)**3
        
    
    def deg_dist_log(self):
        plt.figure(4)
        plt.plot(self.deg_dist.keys(),self.deg_dist.values(),marker='.',linestyle='',label='data')
        plt.yscale('log')
        plt.xscale('log')
        plt.legend()
        plt.ylabel('frequency')
        plt.xlabel('degree k')
        
    
    def deg_writetofile(self,filename='rec_height16.txt'):      #save p(k) and k
        myfile=open(filename,'x')                     # Write the height into a text file
        for k in range(0,max(self.deg_dist)+1):
            myfile.write(str(k) + " " + str(self.deg_dist[k]) + '\n') #
#        print(max(self.deg_dist))    
        myfile.close()  
      
    def nodedeg_writetofile(self,filename='m256.1.106.txt'):      #save p(k) and k
        myfile=open(filename,'x')                     # Write the height into a text file
        for k in range(0,len(self.deglist)):
            myfile.write(str(k) + " " + str(self.deglist[k]) + '\n') #
#        print(max(self.deg_dist))    
        myfile.close()  

#b = BArand()
#b.run(N=100,con=2)
      
        
        