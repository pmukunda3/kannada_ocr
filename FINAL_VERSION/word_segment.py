## Python code for segmentation of Kannada words from a paragraph
## After excecuting this code, open the WordSegmentResult folder
## and make sure that each image contains one (and only ONE) whole Kannada word,
## or a punctation mark. The words should also not be split between several images.
## If the result is not proper then modify the parameters below according to the instructions given

## This is the filename of the image you want to apply OCR on
filename = 'TextSamples/leela (21).png';

## This value should be less than the minimum vertical spacing between two lines of text (in pixels)
## but greater than the maximum vertical spacing between the characters and vattaksharas (subscripts)
## Increase this value if vattaksharas (subscripts) are saved as separate images
## Decrease this value if the words are not in order or words in two different lines appear in a single image                   
ysize = 5;

## This value should be less than the minimum horizontal spacing between two words
## but greater than the maximum horizontal spacing between two letters in a single words
## Increase this value if a single word gets split between multiple images
## Decrease this value if two or more words appear in a single image
xsize = 13;

## This is the threshold value. For most images it is safe to keep this at 128
## (Lesser than 128 will cause errors)
thresh = 150;

## Do NOT modify any of this
import numpy as np
import cv2 as cv
import sys
pwd = sys.path[0]
import os
import shutil
import imgProc_util

dirname = 'WordSegmentResult';
if(os.path.exists("%s/%s"%(pwd,dirname))):
	shutil.rmtree("%s/%s"%(pwd,dirname))
os.mkdir("%s/%s"%(pwd,dirname));

A = cv.imread("%s/%s"%(pwd,filename),cv.IMREAD_GRAYSCALE); 
B = cv.threshold(A,thresh,255,cv.THRESH_BINARY_INV)[1];
X = np.ones((ysize,np.shape(B)[1]));
C = cv.morphologyEx(B,cv.MORPH_CLOSE,X)
N,D = cv.connectedComponents(C)
k = 0;
for i in range(1,N):
  (H,W) = np.where(D == i);
  F = B[min(H):max(H)+1,:];
  ARef = A[min(H):max(H)+1,:];
  base = imgProc_util.getBase(ARef)
  X2 = np.ones((ysize,xsize));
  C2 = cv.morphologyEx(F,cv.MORPH_DILATE,X2)
  C2 = cv.rotate(C2,cv.ROTATE_90_CLOCKWISE);
  N2,D2 = cv.connectedComponentsWithAlgorithm(C2,8,cv.CV_16U,ccltype=cv.CCL_WU);
  D2 = cv.rotate(D2,cv.ROTATE_90_COUNTERCLOCKWISE);
  for j in range(1,N2):
    (H2,W2) = np.where(D2 == j);
    F2 = F[:,min(W2):max(W2)+1];
    ARef2 = ARef[:,min(W2):max(W2)+1];
    (H2,W2) = np.where(F2 != 0);
    final = ARef2[:,min(W2):max(W2)+1];
    filepath = "%s/%s/w%03d_%03d.png"%(pwd,dirname,k,base);
    k = k + 1;
    cv.imwrite(filepath,final);
	
print("Segmentation done. Check the WordSegmentResult folder for proper result, then excecute \"paragraph.py\"");

