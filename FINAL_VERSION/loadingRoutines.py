import numpy as np
import cv2 as cv
import sys
pwd = sys.path[0]
import csv
import os
import fnmatch
from keras.models import load_model

inputShapes = {0:(15,20),1:(25,20),2:(30,20),3:(40,20)}
vattInputShapes = {0:(15,15),1:(20,15),2:(30,15)}
def loadCNNs():
	mainCNN = list()
	vattCNN = list()
	for i in range(4):
		inputShape = inputShapes[i]
		(img_w,img_h) = inputShape
		file = "CNNs/CNN%sx%s.h5" % (img_w,img_h)		
		filepath = "%s/%s"%(pwd,file)
		model = load_model(filepath)
		print("Loaded %s"%file)
		mainCNN.append(model)
	for i in range(3):
		inputShape = vattInputShapes[i]
		(img_w,img_h) = inputShape
		file = "CNNs/VattCNN%sx%s.h5" % (img_w,img_h)
		filepath = "%s/%s"%(pwd,file)
		model = load_model(filepath)
		print("Loaded %s"%file)
		vattCNN.append(model)
	return (mainCNN,vattCNN)

def loadMainTable(): 
	file = "%s/LookupTables/table.csv" % pwd
	reader = csv.DictReader(open(file, 'r'))
	table = {}
	for row in reader:
		uid = int(row['UID'])
		ch0 = int(row['Char0'])
		ch1 = int(row['Char1'])
		table[uid] = (ch0,ch1)
	return table	
	
def loadVattTable(): 
	file = "%s/LookupTables/vatt.csv" % pwd
	reader = csv.DictReader(open(file, 'r'))
	table = {}
	for row in reader:
		uid = int(row['UID'])
		ch0 = int(row['Char0'])
		ch1 = int(row['Char1'])
		table[uid] = (ch0,ch1)
	return table
	
def loadMainTrainData(sizeClass):
	widths = {0:15,1:25,2:30,3:40}
	width = widths[sizeClass]
	dir = "%s/Samples/Resized/Samples%s" % (pwd,width)
	files = os.listdir(dir)
	img_w, img_h = width, 20
	k = 0;
	n = len(files)
	x_train = np.empty((n,img_h,img_w),dtype = 'uint8')
	y_train = np.empty(n,dtype = 'uint16')
	numClasses = 340
	for i in range(numClasses):
		endString = "*%03d.png" % i
		classSet = fnmatch.filter(files,endString)
		for file in classSet:
			img = cv.imread(dir+'/'+file,cv.IMREAD_GRAYSCALE)
			x_train[k,:,:] = img			
			y_train[k] = i
			k = k + 1
	return (x_train,y_train,img_w,img_h)
	
def loadVattTrainData(sizeClass):
	widths = {0:15,1:20,2:30}
	width = widths[sizeClass]
	dir = "%s/Samples/Resized/Vatt%s" % (pwd,width)
	files = os.listdir(dir)
	img_w, img_h = width, 15
	k = 0;
	n = len(files)
	x_train = np.empty((n,img_h,img_w),dtype = 'uint8')
	y_train = np.empty(n,dtype = 'uint16')
	numClasses = 32
	for i in range(numClasses):
		endString = "*%03d.png" % i
		classSet = fnmatch.filter(files,endString)
		for file in classSet:
			img = cv.imread(dir+'/'+file,cv.IMREAD_GRAYSCALE)
			x_train[k,:,:] = img			
			y_train[k] = i
			k = k + 1
	return (x_train,y_train,img_w,img_h)