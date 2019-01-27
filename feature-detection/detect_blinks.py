# import the necessary packages
# To install: dlib and imutils
from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import dlib
import cv2
import argparse

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

def wink_detector(image):
	# Convert image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	print(gray.shape, type(gray[0][1]))
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
	# Get ROI for left and right eyes
	leftEye = shape[lStart:lEnd]
	rightEye = shape[rStart:rEnd]
	# Compute and visualize convex hull
	leftEyeHull = cv2.convexHull(leftEye)
	rightEyeHull = cv2.convexHull(rightEye)

	# Compute eye-aspect-ratio for both eyes
	leftEAR = eye_aspect_ratio(leftEye)
	rightEAR = eye_aspect_ratio(rightEye)
	# Set threshold for eye-aspect-ratio
	EYE_AR_THRESH = 0.24
	print("Left EAR:",str(leftEAR))
	print("Right EAR:",str(rightEAR))
	# Blink with left eye: -1, Blink with right eye: +1, Otherwise return 0
	if leftEAR < EYE_AR_THRESH and rightEAR > EYE_AR_THRESH:
		return -1, [leftEyeHull,rightEyeHull]
	elif leftEAR > EYE_AR_THRESH and rightEAR < EYE_AR_THRESH:
		return 1, [leftEyeHull,rightEyeHull]
	else:
		return 0, [leftEyeHull,rightEyeHull]


