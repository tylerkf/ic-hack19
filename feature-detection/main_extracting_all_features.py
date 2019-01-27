#run the file using the predictor using library
#python main_extracting_all_features.py --shape-predictor shape_predictor_68_face_landmarks.dat
import cv2
import matplotlib.pyplot as plt
import ffdet
import ffdet_st as ffdet2
from face_alignment import *
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import detect_blinks as blinky
from PIL import Image

# Open image files
image = Image.open('image.png')
image = np.asarray(image)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# rough pictures
#capture = cv2.VideoCapture(0)
#facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

# constructing palign class and associated boxes
face_aligner = FaceAligner(predictor)
grayscale = np.average(image,axis=2).astype(np.uint8)
rect = detector(grayscale,0)


# aligning the face and extracting rotation
result = face_aligner.align(image, grayscale, rect[0])
aligned_image = result[0]

if 0 <= -result[1] <= 90 or 180 <= -result[1] <= 270:
	angle = (- result[1]) % 90
else:
	angle = ( - result[1] % 90) - 90

 
# extracting winking and the convex hull
wink_value, eye_landmarks = blinky.wink_detector(aligned_image)
pupil_value = blinky.pupil_detector(grayscale, eye_landmarks)


# dictionary of the features: 
# inclination = -1,0,1 corresponding to left inclination, no incl. or right incl.
# wink_value = -1,0,1 corresponding to winking left eye, not winking or winking right eye
# pupil_value = -1,0,1 corresponding to pointing to the left, neutral or point to the right
inclination = 0
if angle > 10:
	inclination = -1
elif angle < -10:
	inclination = 1

feature_dic = {"head_inclination": inclination, "winking": wink_value, \
			"pupil_direction": pupil_value}

print(feature_dic)

