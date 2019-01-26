import cv2
import time
import matplotlib.pyplot as plt

FACE_CASC_PATH = "haarcascade_frontalface_default.xml"
EYE_CASC_PATH = "haarcascade_eye.xml"

## CV2 feature detection

def detect_faces(face_cascade, image):
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(
    gray_image,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
	)

	return faces

def detect_eyes(eye_cascade, image):
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	eyes = eye_cascade.detectMultiScale(
    gray_image,
    scaleFactor=1.1,
    minNeighbors=8,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
	)

	return eyes

## helper functions

def draw_features(image, features, colour=(0, 255, 0)):
	for (x, y, w, h) in features:
		cv2.rectangle(image, (x, y), (x + w, y + h), colour, 2)

	return image

def create_facial_features(face_features, eye_features):
	facial_features_list = []
	for (fx, fy, fw, fh) in face_features:
		facial_features = {"face": (fx, fy, fw, fh)}
		eyes = []

		for (ex, ey, ew, eh) in eye_features:
			if fx < ex and ex + ew < fx + fw\
					and fy < ey and ey + eh < fy + fh:
				# eye inside face:
				eyes.append((ex, ey, ew, eh))

		n_eyes = len(eyes)
		if n_eyes == 2:
			# correct number of eyes, perfect!
			ex0 = eyes[0][0]
			ex1 = eyes[1][0]
			if ex0 < ex1:
				facial_features["left_eye"] = eyes[0]
				facial_features["right_eye"] = eyes[1]
			else:
				facial_features["right_eye"] = eyes[0]
				facial_features["left_eye"] = eyes[1]
			facial_features_list.append(facial_features)
		elif n_eyes > 2:
			# TODO - pick best eyes
			continue

	return facial_features_list

def get_facial_features_from_capture(capture):
	face_cascade = cv2.CascadeClassifier(FACE_CASC_PATH)
	eye_cascade = cv2.CascadeClassifier(EYE_CASC_PATH)

	response, image = capture.read()

	faces = detect_faces(face_cascade, image)
	eyes = detect_eyes(eye_cascade, image)

	facial_features_list = create_facial_features(faces, eyes)
