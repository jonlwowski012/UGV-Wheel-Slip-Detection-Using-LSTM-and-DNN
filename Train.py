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

# Constant Variables
epochs = 10
batch_size = 10
data_dim = 4
timesteps = 50
num_classes = 1

# Read Dataset
data = pd.read_csv('dataset/fault_dataset.csv')

X = data[['vleft','vright','vx','vw']]
y = data['labels']

print X.shape
print y.shape

# Create LSTM
# expected input data shape: (batch_size, timesteps, data_dim)
model = Sequential()
model.add(LSTM(32, return_sequences=True,
               input_shape=(timesteps, data_dim)))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32))  # return a single vector of dimension 32
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

#model.fit(x_train, y_train,
#          batch_size=64, epochs=5,
#          validation_data=(x_val, y_val))
