import numpy as np
import cv2 as cv
# import matplotlib.pyplot as plt
import sys
pwd = sys.path[0]
import os
import fnmatch

dir = "%s/Vattakshara2" % pwd
dst = "%s/Vattaksharas_CROPPED" % pwd
allFiles = os.listdir(dir)
prefix = "*03?.png"

#fig = plt.figure()

#for i in range(1):
for file in allFiles:
	#file = '13033.png'
	new_img = cv.imread("%s/%s"%(dir,file),cv.IMREAD_GRAYSCALE)
	retval,ref = cv.threshold(new_img,128,255,cv.THRESH_BINARY)
	(H,W) = np.where(ref == 0)
	imgCrop = new_img[min(H):max(H)+1,min(W):max(W)+1]
	w,h = imgCrop.shape[::-1]
	dsize = (int(w*100/h),100)
	#imgCrop = cv.resize(imgCrop,dsize,cv.INTER_CUBIC)
	retval,imgBW = cv.threshold(imgCrop,128,255,cv.THRESH_BINARY)
	img64f = cv.Sobel(imgBW,cv.CV_64F,0,1,ksize=3)
	img2 = np.uint8(img64f)
	vpp = np.sum(img2,1)/255;
	#half = int(vpp.shape[0]/2)
	pc30 = int(vpp.shape[0]*3/10)
	pc70 = int(vpp.shape[0]*7/10)
	pc80 = int(vpp.shape[0]*8/10)
	if(fnmatch.fnmatch(file,prefix)):	
		base = pc30 + np.argmax(vpp[pc30:pc70])
	else:
		base = pc30 + np.argmax(vpp[pc30:pc80])
	imgLower = imgCrop[base+1:,:]
	retval,imgLowerBW = cv.threshold(imgLower,128,255,cv.THRESH_BINARY)
	pc10 = int(imgLowerBW.shape[0]/10)+1
	imgLowerBW[0:pc10] = 255
	(H,W) = np.where(imgLowerBW == 0)
	vatt = imgCrop[base+1:,min(W):max(W)+1]
	cv.imwrite("%s/c%s"%(dst,file),vatt)
	# plt.imshow(vatt,cmap = "gray")
	
# plt.draw()	
# plt.waitforbuttonpress(0)
# plt.close(fig)
