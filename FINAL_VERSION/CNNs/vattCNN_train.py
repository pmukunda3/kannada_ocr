import os.path
import sys
sys.path[0] = os.path.abspath(os.path.join(sys.path[0],'..'))
pwd = sys.path[0]
import keras
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from loadingRoutines import loadVattTrainData
import numpy as np
import matplotlib.pylab as plt
import time

batch_size = 32
num_classes = 32
epochs = 15

for i in range(3):
	# load the data set
	(x_train, y_train,img_w,img_h) = loadVattTrainData(i)
	x_test = x_train 
	y_test = y_train

	# reshape the data into a 4D tensor - (sample_number, x_img_size, y_img_size, num_channels)
	x_train = x_train.reshape(x_train.shape[0], img_w, img_h, 1)
	x_test = x_test.reshape(x_test.shape[0], img_w, img_h, 1)
	input_shape = (img_w, img_h, 1)

	x_train = x_train.astype('float32')
	x_test = x_test.astype('float32')
	x_train /= 255
	x_test /= 255
	print('x_train shape:', x_train.shape)
	print(x_train.shape[0], 'train samples')
	print(x_test.shape[0], 'test samples')

	y_train = keras.utils.to_categorical(y_train, num_classes)
	y_test = keras.utils.to_categorical(y_test, num_classes)

	model = Sequential()
	model.add(Conv2D(64, kernel_size=(5, 5), strides=(1, 1),activation='relu',input_shape=input_shape))
	model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
	model.add(Flatten())
	model.add(Dense(1000, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))

	model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adam(),metrics=['accuracy'])

	model.fit(x_train, y_train,batch_size=batch_size,epochs=epochs,verbose=1)

	score = model.evaluate(x_test, y_test, verbose=0)
	print('Test loss:', score[0])
	print('Test accuracy:', score[1])

	filename = "%s/CNNs/VattCNN%sx%s.h5" % (pwd,img_w,img_h)
	model.save(filename)
	del model
