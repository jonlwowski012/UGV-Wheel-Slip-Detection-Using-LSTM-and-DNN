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

# Constant Variables
epochs = 10
batch_size = 50
data_dim = 6
timesteps = 100000
num_classes = 1
	
# Read Dataset
data = pd.read_csv('../dataset/fault_dataset.csv')

X = data[['posex','posey','orix','oriy','oriz','oriw']]
y = data['labels']

print X.shape
print y.shape

model_dir = 'model'

# Create LSTM
# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
#model.add(Embedding(batch_size, timesteps, input_length=data_dim))
model.add(LSTM(100, input_shape=(1, data_dim), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(75, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(65, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(55))
model.add(Dense(50, activation='sigmoid'))
model.add(Dense(35, activation='sigmoid'))
model.add(Dense(15, activation='sigmoid'))
model.add(Dense(1,  activation='sigmoid'))

model.compile(loss='mse',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(np.reshape(X.as_matrix(), (X.as_matrix().shape[0], 1, X.as_matrix().shape[1])),y.as_matrix(), batch_size=batch_size, epochs=epochs, validation_split= .3)

# Save parameters
config = model.to_json()
open(join(model_dir, 'model_weights.json'), "w").write(config)
model.save_weights(join(model_dir,'model_weights.h5'))
