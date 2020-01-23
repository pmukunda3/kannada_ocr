## Python code to identify words after they have been segmented
## Run this code only after you have excecuted "word_segment.py" and got a proper result
## After excecuting this code, the OCR output will appear in a file called "paragraph.txt"

## This is the threshold value. Keep this somewhere between 100 and 200
## Use lesser value for darker text and greater values for lighter text
## Try modifying this value if you get a runtime error 
## or lot of misplaced 1's or punctuation marks
thresh = 192;

## Keep between 0 and 1
## Reduce if letters are missing
## Increase if you get extra wrong characters between correct characters
accMin = 0.3;

## Do NOT modify any of this
import keras
import sys
pwd = sys.path[0]
from time import time
import getWord
from loadingRoutines import loadCNNs
import numpy as np
import cv2 as cv
import os
import fnmatch
import codecs

def output(filepath,text):
	with codecs.open(filepath,"w+","utf-16") as file:
		file.write(text)
		
mainCNN,vattCNN = loadCNNs()
dir = "%s/WordSegmentResult" % pwd
allFiles = os.listdir(dir)
lines = list()
prefix = "*.png"
someFiles = fnmatch.filter(allFiles,prefix)

for file in someFiles:
	path = "%s/%s" % (dir,file)
	print(file)
	img = cv.imread(path,cv.IMREAD_GRAYSCALE)
	w,h = img.shape[::-1]
	if h <= 5 or w <= 5:
		continue
	base = int(file[-7:-4])
	word = getWord.getWord(img,mainCNN,vattCNN,base=None,thresh=thresh,accMin=accMin)
	lines.append(word)
space = '\x20'
text = space.join(lines)

file = "%s/paragraph.txt" % pwd
output(file,text)

print("Identification done. Your output is stored in the file \"paragraph.txt\"")



