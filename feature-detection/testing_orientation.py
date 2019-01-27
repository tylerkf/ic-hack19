import cv2
import matplotlib.pyplot as plt
import ffdet
from extracting_orientation_feature import *
from dlib import *
# example
capture = cv2.VideoCapture(0)
facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["nose"])

face_aligner = FaceAligner(predictor)
grayscale = np.average(image,axis=2)
rect = cv2.rectangle(image,(384,0),(510,128),(0,255,0),3)

face_aligner.align(image, grayscale, rect)

plt.imshow(image)
plt.show()