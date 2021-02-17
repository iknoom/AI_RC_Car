__author__ = 'will'

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dropout
from keras.layers import Flatten
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle

outputs = 1


from get_image_data import *

trX,trY = get_training_data()
teX,teY = get_test_data()

seed = 0
np.random.seed(seed)
tf.random.set_seed(seed)


# Hyperparameters
nb_classes = 5  # 클래스 수 결정
nb_epochs = 30  # epoch 결정

# channel 차원 추가
trX = trX.reshape(trX.shape[0], 16, 16, 1)
teX = teX.reshape(teX.shape[0], 16, 16, 1)

# One-hot encoding
enc = OneHotEncoder()
enc.fit(trY.reshape(-1, 1))
trY_onehot = enc.transform(trY.reshape(-1, 1)).toarray()
teY_onehot = enc.transform(teY.reshape(-1, 1)).toarray()

# print(f'trX: {trX.shape}')
# print(f'trY: {trY_onehot.shape}')
# print(f'teX: {teX.shape}')
# print(f'teY: {teY_onehot.shape}')

# build model
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same', input_shape=trX.shape[1:], activation='tanh'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same', activation='tanh'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# learning
model.fit(trX, trY_onehot, epochs=nb_epochs, batch_size=1)
print('='*100)

# validation check
Y_prediction = model.predict(teX)

# Previous model
# model=Sequential()
# model.add(Dense(512, input_dim=np.shape(trX)[1], activation='relu'))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(1))
#
# model.compile(loss='mean_squared_error', optimizer='adam')
#
# model.fit(trX, trY, epochs=50, batch_size=1)

Y_prediction = model.predict(teX).flatten()

# validation result
for i in range(teX.shape[0]):
    ans = int(teY[i])
    pred_onehot = Y_prediction[i]
    pred = (np.argmax(pred_onehot, 0) - 2)
    print(f"label: {ans:2d}, predict: {pred:2d}")

# check accuracy
model.evaluate(teX, teY_onehot)

# def get_direction(img):
#     print(img.shape)
# #    img = np.array([np.reshape(img,img.shape**2)])
#     ret =  model.predict(np.array([img]))
#     return ret

# Predict direction with single image
# dir=get_direction(teX[10])
# print(dir[0][0])