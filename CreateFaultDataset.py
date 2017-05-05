
# coding: utf-8

# In[9]:

import csv
import pandas as pd
import numpy as np
from numpy import genfromtxt


# In[15]:

time = genfromtxt('dataset/time.csv', delimiter=',')
vleft = genfromtxt('dataset/vleft.csv', delimiter=',')
vleft_labels = genfromtxt('dataset/vleft_faultlabel.csv', delimiter=',')
vright = genfromtxt('dataset/vright.csv', delimiter=',')
vright_labels = genfromtxt('dataset/vright_faultlabel.csv', delimiter=',')
vx = genfromtxt('dataset/vx.csv', delimiter=',')
vw = genfromtxt('dataset/vw.csv', delimiter=',')
labels = np.logical_or(vleft_labels,vright_labels)


# In[38]:
df = pd.DataFrame({'time':time,'vleft':vleft,'vright':vright,'vx':vx,'vw':vw, 'labels':labels})

df.to_csv('dataset/fault_dataset.csv')






