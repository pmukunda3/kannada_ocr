This is a soft copy of the project titled 'An OCR System for Printed Kannada Text', done by:
- Niraj S Prasad (1PI14EC043)
- Pradyumna Mukunda (1PI14EC045)
- Santhosh D M (1PI14EC060)

The folder contains all the samples used for the project, the implementation codes, and the output text files.

How to setup:
1. Install Python 3.6

2. Install the latest version  of pip

3. Using pip, install the latest version following packages:
	Numpy
	OpenCV
	TensorFlow
	Keras
	
Instructions (How to Use):	
1. Copy the image of the Kannada text into this folder
	
2. Run the code "word_segment.py" in Python 3.6
	NOTE: You need to modify the parameters "filename","ysize","xsize" and "thresh"
	as per the instructions given in the program comments.
	For the samples we have given "sample1.png","sample2.png" etc. use the values
	given in the file "values.txt"
	
3. Run the code "paragraph.py" in Python 3.6
	NOTE: You may need to modify the value of "thresh"
	as per the instructions given in the comments
	
4. Your output will be stored in "paragraph.txt"

We have given a few samples for you to try out:
- sample1.png
- sample2.png
- sample3.png
- sample4.png
- sample5.png