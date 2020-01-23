import sys
pwd = sys.path[0]
import numpy as np
import cv2 as cv
from getChar import getChar,getVatt 
import imgProc_util

def getWord(imgCrop,mainCNN,vattCNN,base=None,thresh=128,accMin=0.5):
	# imgCrop = imgProc_util.selfCrop(img)
	if base == None:
		base = imgProc_util.getBase(imgCrop)	
	imgW,imgH = imgCrop.shape[::-1]
	hThresh = imgH/5

	retval,img2 = cv.threshold(imgCrop,thresh,255,cv.THRESH_BINARY_INV)		
	strel = cv.getStructuringElement(cv.MORPH_RECT,(2,int(imgH/5)))
	img2[0:int(0.9*base),:] = cv.morphologyEx(img2[0:int(0.9*base),:],cv.MORPH_DILATE,strel)
	img2[int(base+0.2*(imgH-base)):,:] = cv.morphologyEx(img2[int(base+0.2*(imgH-base)):,:],cv.MORPH_DILATE,strel)
	N,img2L = cv.connectedComponents(img2,connectivity=8)							## Identifies where the characters are, but labels them in wrong order 
	word = ""
	nativeOrder = []
	prevSize = 0
	kag = False;
	prevKag = kag
	printLast = False
	for lbl in range(1,N):															## Routine to get position of character on w-axis for each label
		(H,W) = np.where(img2L == lbl)
		if (max(H)-min(H) < hThresh):
			continue
		Hhalf = (min(H)+max(H))/2
		Whalf = int((min(W)+max(W))/2)
		if(Hhalf > base):															## Force ordering of vattaksharas after main characters at same w-position
			nativeOrder.append((lbl,Whalf))
		else:
			nativeOrder.append((lbl,min(W)))
	reordered = sorted(nativeOrder,key = lambda x: x[1])							## Sort the characters in proper order, keeping labels intact
	for letter in reordered:
		lbl = letter[0]
		(H,W) = np.where(img2L == lbl)												## List all the pixels constituting a certain character 
		Hhalf = (min(H)+max(H))/2													## Get h-position of character
		if(Hhalf > base):															## For characters below base line (vattakshara)
			mask = 255*np.uint8(img2L == lbl)										## Use masking to create a new image with all other characters removed
			img3 = np.bitwise_and(np.invert(imgCrop),mask)					
			img3 = np.invert(img3)
			img3 = imgProc_util.selfCrop(img3)								
			(vatt,size,acc,printLast) = getVatt(img3,vattCNN)						## Get vattakshara from image
			if (acc < accMin):
				vatt = ''
				size = 0
			if (~printLast & prevKag):												## Procedure for printing vattakshara in Unicode
				prevKagChar = word[-1:]
				word = word[:-1] + vatt + prevKagChar
			else:
				word = word + vatt
			prevSize = prevSize + size		
		else:
			Hmax = max(H)
			img3 = imgCrop[min(H):max(H)+1,min(W):max(W)+1]							## Crop out a single character from word image 			
			img3 = imgProc_util.selfCrop(img3)		
			(char,size,acc,flags) = getChar(img3,mainCNN)							## Get character from image
			(kag,dirga,arka,extraHeight) = flags
			if(imgH-base > 9 and Hmax > (base+(imgH-base)/2) and ~extraHeight):		## Test for joined vatt and character
				img3 = imgCrop[:,min(W):max(W)+1]
				res = imgProc_util.splitChar(img3,base)								## Split image
				if res is not None:
					(imgU,imgL,L_Before_U) = res
					if imgL is not None:
						(char2,size2,acc2,flags) = getChar(imgU,mainCNN)			## Get character from upper part of image
						kag2 = flags[0]
						if(acc2 > acc):
							if(acc2 < accMin):
								continue
							char = char2											## Replace original with new
							size = size2
							kag = kag2						
							(vatt,sizeV,acc,printLast) = getVatt(imgL,vattCNN)		## Get vattakshara from lower part of image
							if(acc < accMin):
								vatt = ''
								sizeV = 0
							if(L_Before_U):											## Procedure to print if character was connected to PREVIOUS vattakshara
								if(~printLast & prevKag):
									prevKagChar = word[-1:]								
									word = word[:-1] + vatt + prevKagChar + char				
								else:
									word = word + vatt + char
								prevSize = size	
							else:													## Prodecure to print if character was connected to NEXT vattakshara
								if(~printLast & kag):									
									kagChar = char[-1:]									
									aksChar = char[:-1]
									word = word + aksChar + vatt + kagChar				
								else:													
									word = word + char + vatt							
								prevSize = size + sizeV	
							prevKag = kag									
							continue												## If character is identifiable and is not arkavattu
			if(acc < accMin):
				continue
			if (arka):																## If character is arkavattu
				prevChar = word[-prevSize:]											## Procedure for printing arkavattu in Unicode
				word = word[:-prevSize] + char + prevChar
			else:
				word = word + char													## Print character normally 
			if(dirga):		
				prevSize = prevSize + size
			else:
				prevSize = size									
			prevKag = kag
	return word

