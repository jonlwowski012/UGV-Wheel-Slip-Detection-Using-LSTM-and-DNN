from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import losses
from os import listdir
from os.path import join
from scipy import misc
import numpy as np
from keras.callbacks import EarlyStopping
from numpy import genfromtxt
import pandas as pd

def shuffler(filename):
	df = pd.read_csv(filename, header=0)
	# return the pandas dataframe
	return df.reindex(np.random.permutation(df.index))
	
	
# Constant Variables
epochs = 1000
batch_size = 1000
data_dim = 6
num_classes = 4
model_dir = 'model'
	
# Read Dataset
data = pd.read_csv('../dataset/fault_dataset.csv')
data = shuffler('../dataset/fault_dataset.csv')

X = np.asarray(data[['posex','posey','orix','oriy','oriz','oriw']])
y_norm = np.asarray(data['labels'])
y = np.zeros((len(y_norm), num_classes))
y[np.arange(len(y_norm)), y_norm] = 1

print y

# Create NN
model = Sequential()
model.add(Dense(24, input_dim=6, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(num_classes, activation='sigmoid'))

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.3)

# Save parameters
config = model.to_json()
open(join(model_dir, 'model_weights.json'), "w").write(config)
model.save_weights(join(model_dir,'model_weights.h5'))
