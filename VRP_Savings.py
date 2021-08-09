#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np


# In[2]:


rnd = np.random
rnd.seed(1)
n = 50
xc = rnd.rand(n+1)*20
yc = rnd.rand(n+1)*10


# In[3]:


plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 200
plt.plot(xc[0], yc[0],c='r',marker='s')
plt.scatter(xc[1:], yc[1:], c='b')


# In[4]:


N = [i for i in range(1, n+1)]
V = [0] + N
A = [(i,j) for i in V for j in V if i!=j]
Distancia = {(i,j): np.hypot(xc[i]-xc[j], yc[i]-yc[j]) for i,j in A}
K = 50
k = {i: rnd.randint(1,10) for i in N}
routes = [[0,i,0,k[i]] for i in range(n+1)   if i>0]


# In[5]:


Distancia


# In[6]:


k


# In[7]:


routes


# In[8]:


def cw_savings():
    savings = [(Distancia[i,0]+Distancia[0,j]-Distancia[i,j], i, j) for i,j in Distancia if i!=j and i>0 and j>0 and i>j]
    savings.sort(reverse=True)
    return savings


# In[9]:


def find_node(node, routes):
    for i in range(len(routes)):
        if node in routes[i] and routes[i].index(node) != (len(routes[i])-1):
            return i, routes[i].index(node)


# In[10]:


def test_merge(idr1, idn1 ,idr2, idn2, routes):
    if idr1 == idr2:
        return 0
    if routes[idr1][idn1+1] == 0 and routes[idr2][idn2-1] == 0:
        if routes[idr1][-1] + routes[idr2][-1] < K:
            return 1
        else:
            return 0
    if routes[idr1][idn1-1] == 0 and routes[idr2][idn2+1] == 0:
        if routes[idr1][-1] + routes[idr2][-1] < K:
            return 2
        else:
            return 0
    else:
        return 0


# In[11]:


def merge(idr1,idr2,routes):
    t1,t2 = routes[idr1], routes[idr2]
    t3 = t1[:-2] + t2[1:-1] + [(t1[-1] + t2[-1])]
    routes.append(t3)
    routes.remove(t1)
    routes.remove(t2)
   # print(routes)


# In[12]:


def sequential_savings(savings, routes):
    while len(savings) > 0:
        idr1,idn1 = find_node(savings[0][1], routes)
        idr2,idn2 = find_node(savings[0][2], routes)
        test = test_merge(idr1,idn1,idr2,idn2,routes)
        
        #print("status:" ,test)
        if test == 1:
            merge(idr1,idr2,routes)
        
        if test == 2:
            merge(idr2,idr1,routes)
        savings.pop(0)
    return routes


# In[13]:


savings = cw_savings()
savings


# In[14]:



sequential_savings(savings,routes)


# In[15]:


auxiliar = [(routes[i][j],routes[i][j+1]) for i in range(len(routes)) for j in range(len(routes[i])-2)]


# In[16]:


plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['figure.dpi'] = 200
plt.plot(xc[0], yc[0],c='r',marker='s')
plt.scatter(xc[1:], yc[1:], c='b')
for i, j in auxiliar:
    plt.plot([xc[i],xc[j]],[yc[i],yc[j]],zorder=0, c='purple')

