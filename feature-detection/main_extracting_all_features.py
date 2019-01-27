#run the file using the predictor using library
#python main_extracting_all_features.py --shape-predictor shape_predictor_68_face_landmarks.dat
import cv2
import matplotlib.pyplot as plt
import ffdet_st as ffdet
from face_alignment import *
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import detect_blinks as blinky
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])


capture = cv2.VideoCapture(0)
facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

face_aligner = FaceAligner(predictor)
grayscale = np.average(image,axis=2).astype(np.uint8)

print(type(grayscale[1][1]),grayscale.shape)
rect = detector(grayscale,0)

result = face_aligner.align(image, grayscale, rect[0])
aligned_image = result[0]

if 0 <= -result[1] <= 90 or 180 <= -result[1] <= 270:
	angle = (- result[1]) % 90
else:
	angle = ( - result[1] % 90) - 90

plt.imshow(aligned_image)
plt.show()