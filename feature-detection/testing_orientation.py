#run the file using the predictor using library
#python 
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

rect = detector(grayscale,0)

result = face_aligner.align(image, grayscale, rect[0])
aligned_image = result[0]

if 0 <= -result[1] <= 90 or 180 <= -result[1] <= 270:
	angle = (- result[1]) % 90
else:
	angle = ( - result[1] % 90) - 90


wink_value, convexhull = blinky.wink_detector(image)
if wink_value == -1:
	print("Ah, you winked with your left eye!")
elif wink_value == 1:
	print("Ah, you winked with your right eye!")
else:
	print("You didn't wink!")
cv2.drawContours(image, [convexhull[0]], -1, (0, 255, 0), 1)
cv2.drawContours(image, [convexhull[1]], -1, (0, 255, 0), 1)
cv2.imshow("Image", image)

if facial_features_list:
	features = facial_features_list[0]
	image = ffdet.draw_features(image, [features["face"]], (255, 0, 0))
	image = ffdet.draw_features(image, [features["left_eye"]], (0, 255, 0))
	image = ffdet.draw_features(image, [features["right_eye"]], (0, 0, 255))
	face_xy = features["face"]
	left_eye_xy = features["left_eye"]
	right_eye_xy = features["right_eye"]
	face_roi = image[face_xy[1]:face_xy[1]+face_xy[3], \
				face_xy[0]:face_xy[0]+face_xy[2]]
	left_eye_roi = image[left_eye_xy[1]:left_eye_xy[1]+left_eye_xy[3], \
				left_eye_xy[0]:left_eye_xy[0]+left_eye_xy[2]]
	right_eye_roi = image[right_eye_xy[1]:right_eye_xy[1]+right_eye_xy[3],\
			right_eye_xy[0]:right_eye_xy[0]+right_eye_xy[2]]
	cv2.imshow("FACE", face_roi)
	cv2.imshow("LEFT_EYE", left_eye_roi)
	cv2.imshow("RIGHT_EYE", right_eye_roi)
else:
	print("no features found!")


print(angle)

plt.imshow(aligned_image)
plt.show()