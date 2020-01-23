import numpy as np

def cnn_predict(img,model,input_shape):
	(img_w,img_h) = input_shape
	x_test = img.reshape(1,img_w, img_h, 1)
	x_test = x_test.astype('float32')
	x_test /= 255
	
	y_pred = model.predict(x_test)
	maxVal = np.max(y_pred,1)
	idx = np.argmax(y_pred,1)
	y_pred[0,idx] = 0
	nextMaxVal = np.max(y_pred,1)
	return idx[0], maxVal[0]
