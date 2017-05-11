import numpy as np
from scipy.misc import imread, imsave, imresize
from keras.models import model_from_json
from os.path import join
import matplotlib.pyplot as plt
import pandas as pd
import time

def shuffler(filename):
	df = pd.read_csv(filename, header=0)
	# return the pandas dataframe
	return df.reindex(np.random.permutation(df.index))


num_classes = 4
# Read Dataset
data = pd.read_csv('../dataset/fault_dataset.csv')
data = shuffler('../dataset/fault_dataset.csv')
X = np.asarray(data[['posex','posey','orix','oriy','oriz','oriw']])
y_norm = np.asarray(data['labels'])
y = np.zeros((len(y_norm), num_classes))
y[np.arange(len(y_norm)), y_norm] = 1

# Define Paths and Variables
model_dir = 'model'

#%% Load model and weights separately due to error in keras
model = model_from_json(open(model_dir+"/model_weights.json").read())
model.load_weights(model_dir+"/model_weights.h5")


#%% Predict Output
t0 = time.time()
output_org = model.predict(np.reshape(X, (X.shape[0], 1, X.shape[1])))
print "Time to predict all ", len(X), " samples: ", time.time()-t0
print "Average time to predict a sample: ", (time.time()-t0)/len(X) 

output = np.zeros_like(output_org)
output[np.arange(len(output_org)), output_org.argmax(1)] = 1

correct = 0
for i in range(len(output)):
	if np.array_equal(output[i],y[i]):
		correct += 1

print "Acc: ", correct/float(len(output))

output_index = []
for row in output:
	output_index.append(np.argmax(row))

plt.plot(y_norm, color='red',linewidth=3)
plt.plot(output_index, color='blue', linewidth=1)
plt.show()
