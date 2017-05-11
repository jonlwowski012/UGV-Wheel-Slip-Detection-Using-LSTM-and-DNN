
# coding: utf-8

# In[9]:

import csv
import pandas as pd
import numpy as np
from numpy import genfromtxt


# In[15]:

d_one = pd.read_csv('bags/faulty/bagfile-_odom.csv',sep=',',engine='python',header=0)
d_two = pd.read_csv('bags/faulty/bagfile-_mobile_base_commands_velocity.csv',sep=',',engine='python',header=0)
d_three = pd.merge(d_one, d_two, on='%time', how='outer')
d_three.to_csv('bags/faulty/faulty_output.csv',sep=',')

d_one = pd.read_csv('bags/nonfaulty/bagfile-_odom.csv',sep=',',engine='python',header=0)
d_two = pd.read_csv('bags/nonfaulty/bagfile-_mobile_base_commands_velocity.csv',sep=',',engine='python',header=0)
d_three = pd.merge(d_one, d_two, on='%time', how='outer')
d_three.to_csv('bags/nonfaulty/nonfaulty_output.csv',sep=',')

faulty = genfromtxt('bags/faulty/faulty_output.csv', delimiter=',')
nonfaulty = genfromtxt('bags/nonfaulty/nonfaulty_output.csv', delimiter=',')

fposex = []
fposey = []
forix = []
foriy = []
foriz = []
foriw = []
fvelx = []
fangz = []

nfposex = []
nfposey = []
nforix = []
nforiy = []
nforiz = []
nforiw = []
nfvelx = []
nfangz = []

labels = []

for row in faulty:
	fposex.append(row[6])
	fposey.append(row[7])
	forix.append(row[9])
	foriy.append(row[10])
	foriz.append(row[11])
	foriw.append(row[12])
	fvelx.append(row[49])
	fangz.append(row[54])
	labels.append(1)
	
for row in nonfaulty:
	nfposex.append(row[6])
	nfposey.append(row[7])
	nforix.append(row[9])
	nforiy.append(row[10])
	nforiz.append(row[11])
	nforiw.append(row[12])
	nfvelx.append(row[49])
	nfangz.append(row[54])
	labels.append(0)
	
	

print np.hstack((fvelx,nfvelx)).shape	
print np.hstack((fposex,nfposex)).shape	


# In[38]:
df = pd.DataFrame({'posex':np.hstack((fposex,nfposex)),'posey':np.hstack((fposey,nfposey)),'orix':np.hstack((forix,nforix)),'oriy':np.hstack((foriy,nforiy)),'oriz':np.hstack((foriz,nforiz)), 'oriw':np.hstack((foriw,nforiw)), 'labels':np.asarray(labels)})

df.to_csv('dataset/fault_dataset.csv')






