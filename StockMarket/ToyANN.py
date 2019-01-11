import re
import time
import random
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import keras
import tensorflow as tf
from keras.utils import to_categorical
from keras.layers import Input, Dense
from keras.models import Model, Sequential

# s = 15
# random.seed(6+s)
# tf.set_random_seed(333+s*2)
# np.random.seed(856+s*3)

split_percent = 0.8
split_idx = round(split_percent*1000)
###
############
############
t = np.linspace(0,2*np.pi,int(1000/2))
x1 = 0.5*(np.cos(t))
y1 = 0.5*(np.sin(t))
labels1 = np.zeros(len(t))
x2 = (np.cos(t))
y2 = (np.sin(t))
labels2 = np.ones(len(t))
x = np.concatenate((x1, x2))
y = np.concatenate((y1, y2))
xy_data = np.column_stack((x, y))
xy_labels = np.concatenate((labels1, labels2))
order = random.sample(range(xy_data.shape[0]), xy_data.shape[0])
xy_data = xy_data[order,:]
xy_labels = xy_labels[order]
train_data = xy_data[:split_idx,:]
train_labels = xy_labels[:split_idx]
test_data = xy_data[split_idx:,:]
test_labels = xy_labels[split_idx:]
##########
##########
train_labels_a = train_labels
test_labels_a = test_labels
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
###
print('Creating Model')
model = Sequential()
model.add(Dense(4, input_dim=2, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(2, activation='softmax'))
omt = keras.optimizers.Adam(lr=0.005)
loss='categorical_crossentropy'
print('Compiling Model')
model.compile(loss=loss,
              optimizer=omt,
              metrics=['accuracy'])
print('Fitting Model')
model.fit(train_data, train_labels,
          epochs=10,
          verbose=True,
          shuffle=True,
          validation_data=(test_data, test_labels))
scoresTest = model.evaluate(test_data, test_labels,verbose=0)
prd = model.predict_classes(test_data)
print(np.column_stack((prd,test_labels_a)))
print(str(model.metrics_names[1])+' %.2f%%' % (scoresTest[1]*100) + ' accuracy on test data')
