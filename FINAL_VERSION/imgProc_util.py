import numpy as np
import cv2 as cv
import sys
pwd = sys.path[0]

def selfCrop(img,thresh=128):
	retval,imgBW = cv.threshold(img,thresh,255,cv.THRESH_BINARY)	
	(H,W) = np.where(imgBW == 0)
	imgCrop = img[min(H):max(H)+1,min(W):max(W)+1]
	return imgCrop

def getBase(imgCrop):
	retval,imgCrop_BW = cv.threshold(imgCrop,128,255,cv.THRESH_BINARY)
	img_HorzEdge = np.uint8(cv.Sobel(imgCrop_BW,cv.CV_64F,0,1,ksize=3))
	hpp = np.sum(img_HorzEdge,1)/255;
	Hhalf = int(hpp.shape[0]/2)
	base = Hhalf + np.argmax(hpp[Hhalf:])
	return base
	
def splitChar(imgCrop,base):
	imgU = imgCrop[0:base+1,:]
	imgL = imgCrop[base+1:,:]
	if list(imgL) == []:
		return None
		
	retval,imgU_BW = cv.threshold(imgU,128,255,cv.THRESH_BINARY)
	(Hu,Wu) = np.where(imgU_BW == 0)
	U_Wpos = int((min(Wu)+max(Wu))/2)
	w,h = imgL.shape[::-1]
	retval,imgL_BW = cv.threshold(imgL,128,255,cv.THRESH_BINARY)
	imgL_BW[0:int(h/5),:] = 255
	(Hl,Wl) = np.where(imgL_BW == 0)
	if (list(Wl) != []):
		L_Wpos = max(Wl)
		L_Before_U = L_Wpos < U_Wpos
	else:
		L_Before_U = False
		
	if (L_Before_U):
		imgU = imgU[:,max(Wl)+1:]
	else:
		imgU_VertEdge = np.uint8(cv.Sobel(imgU_BW,cv.CV_64F,1,0,ksize=3))
		vppU = np.sum(imgU_VertEdge,0)/255;
		Whalf = int(vppU.shape[0]/2)
		rightEdge = Whalf + np.argmax(vppU[Whalf:])
		imgU = imgU[:,0:rightEdge+1]
		
	if (list(Wl) == []):
		imgL = None
	else:
		imgL = imgL[:,min(Wl):max(Wl)+1]
	
	return (imgU,imgL,L_Before_U)