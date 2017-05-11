from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras.optimizers import Adam
from keras import losses
from os import listdir
from os.path import join
from scipy import misc
import numpy as np
from keras.callbacks import EarlyStopping
from numpy import genfromtxt
import pandas as pd
import tensorflow as tf


def shuffler(filename):
	df = pd.read_csv(filename, header=0)
	# return the pandas dataframe
	return df.reindex(np.random.permutation(df.index))
	
	
# Constant Variables
epochs = 75
batch_size = 100
data_dim = 6
timesteps = 100000
num_classes = 4
	
# Read Dataset
data = pd.read_csv('../dataset/fault_dataset.csv')
data = shuffler('../dataset/fault_dataset.csv')

X = data[['posex','posey','orix','oriy','oriz','oriw']]
y_norm = np.asarray(data['labels'])
y = np.zeros((len(y_norm), num_classes))
y[np.arange(len(y_norm)), y_norm] = 1

print X.shape
print y.shape

model_dir = 'model'

# Create LSTM
# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
#model.add(Embedding(batch_size, timesteps, input_length=data_dim))
model.add(LSTM(500, input_shape=(1, data_dim), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(375, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(325, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(275))
model.add(Dense(50, activation='relu'))
model.add(Dense(35, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(num_classes,  activation='sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(np.reshape(X.as_matrix(), (X.as_matrix().shape[0], 1, X.as_matrix().shape[1])),y, batch_size=batch_size, epochs=epochs, validation_split= .3)

# Save parameters
config = model.to_json()
open(join(model_dir, 'model_weights.json'), "w").write(config)
model.save_weights(join(model_dir,'model_weights.h5'))
