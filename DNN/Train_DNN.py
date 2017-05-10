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

# Constant Variables
epochs = 100
batch_size = 100
data_dim = 6
num_classes = 1
model_dir = 'model'
	
# Read Dataset
data = pd.read_csv('../dataset/fault_dataset.csv')

X = np.asarray(data[['posex','posey','orix','oriy','oriz','oriw']])
y = np.asarray(data['labels'])

print X.shape
print y.shape

# Create NN
model = Sequential()
model.add(Dense(12, input_dim=6, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=0.3)

# Save parameters
config = model.to_json()
open(join(model_dir, 'model_weights.json'), "w").write(config)
model.save_weights(join(model_dir,'model_weights.h5'))
