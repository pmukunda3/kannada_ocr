import os
import sys
pwd = sys.path[0] + '/'
import cv2 as cv
import numpy as np
#import fnmatch

dir = pwd + 'Vattaksharas'
files = os.listdir(dir)
#set = fnmatch.filter(files,'*003.png')
n = len(files)
Hsum = 0
Wsum = 0
W15sum = 0
for file in files:
	img = cv.imread(dir+'/'+file,cv.IMREAD_GRAYSCALE)
	w,h = img.shape[::-1]
	ar = w/h
	w15 = ar*15
	Hsum = Hsum + h
	Wsum = Wsum + w
	W15sum = W15sum + w15
Havg = Hsum/n	
Wavg = Wsum/n
W15avg = W15sum/n
print(Havg)
print(Wavg)
print(W15avg)