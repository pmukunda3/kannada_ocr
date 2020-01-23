import numpy as np
import cv2 as cv
import sys
pwd = sys.path[0]
from cnn_predict import cnn_predict
import loadingRoutines


inputShapes = {0:(15,20),1:(25,20),2:(30,20),3:(40,20)}
vattInputShapes = {0:(15,15),1:(20,15),2:(30,15)}
tableM = loadingRoutines.loadMainTable()
tableV = loadingRoutines.loadVattTable()

def getChar(img,CNN):
	w,h = img.shape[::-1]
	ar = w/h
	w20 = ar*20
	if w20 <= 20:
		sizeClass = 0
	elif w20 <= 25:
		sizeClass = 1
	elif w20 < 35:
		sizeClass = 2
	else:
		sizeClass = 3
	inputShape = inputShapes[sizeClass]
	img = cv.resize(img,inputShape,interpolation = cv.INTER_CUBIC)

	(img_w,img_h) = inputShape
	(idx,metric) = cnn_predict(img,CNN[sizeClass],inputShape)
	dirga = (idx == 1)
	arka = (idx == 2)
	extraHeight = (idx >= 43 and idx <= 51) #gha
	extraHeight = extraHeight or (idx >= 62 and idx <= 70) #chha
	extraHeight = extraHeight or (idx >= 80 and idx <= 88) #jha
	extraHeight = extraHeight or (idx >= 116 and idx <= 123) #ddha
	extraHeight = extraHeight or (idx >= 143 and idx <= 151) #tha
	extraHeight = extraHeight or (idx >= 161 and idx <= 169) #dha
	extraHeight = extraHeight or (idx >= 188 and idx <= 196) #pha
	extraHeight = extraHeight or (idx >= 206 and idx <= 214) #bha
	extraHeight = extraHeight or (idx == 182 or idx == 183 or idx == 185)
	extraHeight = extraHeight or (idx == 263 or idx == 264 or idx == 266)
	extraHeight = extraHeight or (idx >= 318 and idx <= 320)
	extraHeight = extraHeight or (idx == 326)
	charseq = tableM[idx]
	if charseq[1] == 0:
		kag = False;
		charSize = 1
		char = chr(charseq[0])
	else:
		kag = True;
		charSize = 2
		char = chr(charseq[0]) + chr(charseq[1])
	flags = (kag,dirga,arka,extraHeight)
	return char,charSize,metric,flags

def getVatt(img,CNN):
	w,h = img.shape[::-1]
	ar = w/h
	w15 = ar*15
	if w15 <= 20:
		sizeClass = 0
	elif w15 <= 25:
		sizeClass = 1
	elif w15 > 25:
		sizeClass = 2
	inputShape = vattInputShapes[sizeClass]
	img = cv.resize(img,inputShape,interpolation = cv.INTER_CUBIC)
	(img_w,img_h) = inputShape
	(idx,metric) = cnn_predict(img,CNN[sizeClass],inputShape)
	printLast = (idx == 1 or idx == 30 or idx == 31)
	charseq = tableV[idx]
	if charseq[1] == 0:
		charSize = 1
		char = chr(charseq[0])
	else:
		charSize = 2
		char = chr(charseq[0]) + chr(charseq[1])
	return char,charSize,metric,printLast

