# Copyright Reserved (2020).
# Donghee Lee, Univ. of Seoul
#
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

class CNN_Driver():
    def __init__(self):
        self.trX = None
        self.trY = None
        self.teX = None
        self.teY = None
        self.model = None

    def keras_learn(self):
        self.trX, self.trY = get_training_data()
        self.teX, self.teY = get_test_data()

        seed = 0
        np.random.seed(seed)
        tf.random.set_seed(seed)

        # Hyperparameters
        nb_classes = 3  # 클래스 수 결정
        nb_epochs = 15  # epoch 결정

        # channel 차원 추가
        self.trX = self.trX.reshape(self.trX.shape[0], 16, 16, 1)
        self.teX = self.teX.reshape(self.teX.shape[0], 16, 16, 1)

        # One-hot encoding
        enc = OneHotEncoder()
        enc.fit(self.trY.reshape(-1, 1))
        trY_onehot = enc.transform(self.trY.reshape(-1, 1)).toarray()
        teY_onehot = enc.transform(self.teY.reshape(-1, 1)).toarray()

        # build model
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), padding='same', input_shape=self.trX.shape[1:], activation='tanh'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Conv2D(64, (3, 3), padding='same', activation='tanh'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(nb_classes, activation='softmax'))

        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # learning
        self.model.fit(self.trX, trY_onehot, epochs=nb_epochs, batch_size=1)
        print('=' * 100)
        return

    def predict_direction(self, img):
        img = img.reshape(1, 16, 16, 1)
        ret = self.model.predict(img)
        ret = np.argmax(ret[0]) - 1
        return ret

    def get_test_img(self):
        img = self.teX[150]
        return img