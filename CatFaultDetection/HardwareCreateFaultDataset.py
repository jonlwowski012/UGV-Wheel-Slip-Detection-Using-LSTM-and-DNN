
# coding: utf-8

# In[9]:

import csv
import pandas as pd
import numpy as np
from numpy import genfromtxt


# In[15]:

d_one = pd.read_csv('bags/left_faulty/bagfile-_odom.csv',sep=',',engine='python',header=0)
d_two = pd.read_csv('bags/left_faulty/bagfile-_mobile_base_commands_velocity.csv',sep=',',engine='python',header=0)
d_three = pd.merge(d_one, d_two, on='%time', how='outer')
d_three.to_csv('bags/left_faulty/left_faulty_output.csv',sep=',')

d_one = pd.read_csv('bags/right_faulty/bagfile-_odom.csv',sep=',',engine='python',header=0)
d_two = pd.read_csv('bags/right_faulty/bagfile-_mobile_base_commands_velocity.csv',sep=',',engine='python',header=0)
d_three = pd.merge(d_one, d_two, on='%time', how='outer')
d_three.to_csv('bags/right_faulty/right_faulty_output.csv',sep=',')

d_one = pd.read_csv('bags/both_faulty/bagfile-_odom.csv',sep=',',engine='python',header=0)
d_two = pd.read_csv('bags/both_faulty/bagfile-_mobile_base_commands_velocity.csv',sep=',',engine='python',header=0)
d_three = pd.merge(d_one, d_two, on='%time', how='outer')
d_three.to_csv('bags/both_faulty/both_faulty_output.csv',sep=',')

d_one = pd.read_csv('bags/nonfaulty/bagfile-_odom.csv',sep=',',engine='python',header=0)
d_two = pd.read_csv('bags/nonfaulty/bagfile-_mobile_base_commands_velocity.csv',sep=',',engine='python',header=0)
d_three = pd.merge(d_one, d_two, on='%time', how='outer')
d_three.to_csv('bags/nonfaulty/nonfaulty_output.csv',sep=',')

left_faulty = genfromtxt('bags/left_faulty/left_faulty_output.csv', delimiter=',')
right_faulty = genfromtxt('bags/right_faulty/right_faulty_output.csv', delimiter=',')
both_faulty = genfromtxt('bags/both_faulty/both_faulty_output.csv', delimiter=',')
nonfaulty = genfromtxt('bags/nonfaulty/nonfaulty_output.csv', delimiter=',')

lfposex = []
lfposey = []
lforix = []
lforiy = []
lforiz = []
lforiw = []
lfvelx = []
lfangz = []

rfposex = []
rfposey = []
rforix = []
rforiy = []
rforiz = []
rforiw = []
rfvelx = []
rfangz = []

bfposex = []
bfposey = []
bforix = []
bforiy = []
bforiz = []
bforiw = []
bfvelx = []
bfangz = []

nfposex = []
nfposey = []
nforix = []
nforiy = []
nforiz = []
nforiw = []
nfvelx = []
nfangz = []

labels = []

for row in left_faulty:
	lfposex.append(row[6])
	lfposey.append(row[7])
	lforix.append(row[9])
	lforiy.append(row[10])
	lforiz.append(row[11])
	lforiw.append(row[12])
	lfvelx.append(row[49])
	lfangz.append(row[54])
	labels.append(1)
	
for row in right_faulty:
	rfposex.append(row[6])
	rfposey.append(row[7])
	rforix.append(row[9])
	rforiy.append(row[10])
	rforiz.append(row[11])
	rforiw.append(row[12])
	rfvelx.append(row[49])
	rfangz.append(row[54])
	labels.append(2)
	
for row in both_faulty:
	bfposex.append(row[6])
	bfposey.append(row[7])
	bforix.append(row[9])
	bforiy.append(row[10])
	bforiz.append(row[11])
	bforiw.append(row[12])
	bfvelx.append(row[49])
	bfangz.append(row[54])
	labels.append(3)
	
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
		


# In[38]:
df = pd.DataFrame({'posex':np.hstack((lfposex,rfposex,bfposex,nfposex)),'posey':np.hstack((lfposey,rfposey,bfposey,nfposey)),'orix':np.hstack((lforix,rforix,bforix,nforix)),'oriy':np.hstack((lforiy,rforiy,bforiy,nforiy)),'oriz':np.hstack((lforiz,rforiz,bforiz,nforiz)), 'oriw':np.hstack((lforiw,rforiw,bforiw,nforiw)), 'labels':np.asarray(labels)})

df.to_csv('dataset/fault_dataset.csv')






