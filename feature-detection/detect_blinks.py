# import the necessary packages
# To install: dlib and imutils
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import cv2
import argparse
import numpy as np
import statistics
from matplotlib import pyplot as plt

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])
	# compute the eye aspect ratio
	EAR = (A + B) / (2.0 * C)
	# return the eye aspect ratio
	return EAR

def createLineIterator(P1, P2, img):
    """
    Produces and array that consists of the coordinates and intensities of each pixel in a line between two points

    Parameters:
        -P1: a numpy array that consists of the coordinate of the first point (x,y)
        -P2: a numpy array that consists of the coordinate of the second point (x,y)
        -img: the image being processed

    Returns:
        -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity])     
    """
   #define local variables for readability
    imageH = img.shape[0]
    imageW = img.shape[1]
    P1X = P1[0]
    P1Y = P1[1]
    P2X = P2[0]
    P2Y = P2[1]

   #difference and absolute difference between points
   #used to calculate slope and relative location between points
    dX = P2X - P1X
    dY = P2Y - P1Y
    dXa = np.abs(dX)
    dYa = np.abs(dY)

   #predefine numpy array for output based on distance between points
    itbuffer = np.empty(shape=(np.maximum(dYa,dXa),3),dtype=np.float32)
    itbuffer.fill(np.nan)

   #Obtain coordinates along the line using a form of Bresenham's algorithm
    negY = P1Y > P2Y
    negX = P1X > P2X
    if P1X == P2X: #vertical line segment
        itbuffer[:,0] = P1X
        if negY:
            itbuffer[:,1] = np.arange(P1Y - 1,P1Y - dYa - 1,-1)
        else:
            itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)              
    elif P1Y == P2Y: #horizontal line segment
        itbuffer[:,1] = P1Y
        if negX:
            itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
        else:
            itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
    else: #diagonal line segment
        steepSlope = dYa > dXa
        if steepSlope:
            slope = dX.astype(np.float32)/dY.astype(np.float32)
            if negY:
                itbuffer[:,1] = np.arange(P1Y-1,P1Y-dYa-1,-1)
            else:
                itbuffer[:,1] = np.arange(P1Y+1,P1Y+dYa+1)
            itbuffer[:,0] = (slope*(itbuffer[:,1]-P1Y)).astype(np.int) + P1X
        else:
            slope = dY.astype(np.float32)/dX.astype(np.float32)
            if negX:
                itbuffer[:,0] = np.arange(P1X-1,P1X-dXa-1,-1)
            else:
                itbuffer[:,0] = np.arange(P1X+1,P1X+dXa+1)
            itbuffer[:,1] = (slope*(itbuffer[:,0]-P1X)).astype(np.int) + P1Y

    #Remove points outside of image
    colX = itbuffer[:,0]
    colY = itbuffer[:,1]
    itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

    #Get intensities from img ndarray
    itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)] 
    itbuffer[:,2] = itbuffer[:,2] - np.min(itbuffer[:,2])
    itbuffer[:,2] = itbuffer[:,2]/np.max(itbuffer[:,2])
    min_val = np.min(itbuffer[:, 2])
    indicator = (itbuffer[:, 2] == min_val)
    total_indicator = np.sum(indicator)
    cum_indicator = 0
    x_pupil = 0
    while x_pupil < indicator.shape[0]:
    	cum_indicator += indicator[x_pupil]
    	if (cum_indicator >= total_indicator/2):
    		break
    	x_pupil += 1
    image_high_cut_bin = cv2.threshold(itbuffer[:,2], 0.2, 1.0, cv2.THRESH_BINARY)[1]

    pupil_left = 0
    pupil_right = 0
    for x in range(0, x_pupil):
    	if image_high_cut_bin[x_pupil - x] == 1:
    		pupil_left = x_pupil - x
    		break

    for x in range(x_pupil, len(itbuffer[:,2])):
    	if image_high_cut_bin[x] == 1:
    		pupil_right = x
    		break

    print(0, pupil_left, pupil_right, len(itbuffer[:,2]))
    ratio = pupil_left/(len(itbuffer[:,2])-pupil_right)

    return itbuffer, ratio

def wink_detector(image):
	# Convert image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--shape-predictor", required=True,
		help="path to facial landmark predictor")
	args = vars(ap.parse_args())
	# Initialise
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(args["shape_predictor"])
	# Obtain landmark indices for left and right eyes
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
	rect = detector(gray, 0)
	shape = predictor(gray, rect[0])
	shape = face_utils.shape_to_np(shape)
	# Get landmarks for left and right eyes
	leftEye = shape[lStart:lEnd]
	rightEye = shape[rStart:rEnd]

	# Compute eye-aspect-ratio for both eyes
	leftEAR = eye_aspect_ratio(leftEye)
	rightEAR = eye_aspect_ratio(rightEye)
	# Set threshold for eye-aspect-ratio
	EYE_AR_THRESH = 0.24
	print("Left EAR:",str(leftEAR))
	print("Right EAR:",str(rightEAR))
	# Blink with left eye: -1, Blink with right eye: +1, Otherwise return 0
	if (leftEAR < EYE_AR_THRESH) & (rightEAR > EYE_AR_THRESH):
		return -1, [leftEye,rightEye]
	elif (leftEAR > EYE_AR_THRESH) & (rightEAR < EYE_AR_THRESH):
		return 1, [leftEye,rightEye]
	else:
		return 0, [leftEye,rightEye]

def pupil_detector(gray_image, eye_landmarks):
	# Convert image to grayscale
	[l_landmarks, r_landmarks] = eye_landmarks	
	l_eye, l_ratio = createLineIterator(l_landmarks[0], l_landmarks[3], gray_image)
	r_eye, r_ratio = createLineIterator(r_landmarks[0], r_landmarks[3], gray_image)
	ratio = (l_ratio+r_ratio)/2
	# Looked left: -1, looked right: +1, neutral: 0 
	if ratio < 0.7:
		return -1
	elif ratio > 1.3:
		return 1
	else:
		return 0 

	
	



