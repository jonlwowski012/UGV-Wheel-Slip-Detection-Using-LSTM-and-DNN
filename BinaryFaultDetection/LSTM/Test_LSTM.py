import numpy as np
from scipy.misc import imread, imsave, imresize
from keras.models import model_from_json
from keras.layers import Embedding
from keras.layers import LSTM
from os.path import join
import matplotlib.pyplot as plt
import pandas as pd
import time

def shuffler(filename):
	df = pd.read_csv(filename, header=0)
	# return the pandas dataframe
	return df.reindex(np.random.permutation(df.index))
	
t0 = time.time()

# Read Dataset
data = pd.read_csv('../dataset/fault_dataset.csv')
#data = shuffler('../dataset/fault_dataset.csv')
X = np.asarray(data[['posex','posey','orix','oriy','oriz','oriw']])
y = np.asarray(data['labels'])

# Define Paths and Variables
model_dir = 'model'

#%% Load model and weights separately due to error in keras
model = model_from_json(open(model_dir+"/model_weights.json").read())
model.load_weights(model_dir+"/model_weights.h5")


#%% Predict Output
output = model.predict(np.reshape(X, (X.shape[0], 1, X.shape[1])))

idx = output > 0.5
idy = output <= 0.5
output[idx] = True
output[idy] = False

correct = 0
for i in range(len(output)):
	if output[i][0] == y[i]:
		correct += 1

print "Acc: ", correct/float(len(output))

plt.plot(y, color='red',linewidth=3)
plt.plot(output, color='blue', linewidth=1)
plt.show()
