import cv2
import matplotlib.pyplot as plt
import ffdet

# example
capture = cv2.VideoCapture(0)
facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

if facial_features_list:
	features = facial_features_list[0]
	image = ffdet.draw_features(image, [features["face"]], (255, 0, 0))
	image = ffdet.draw_features(image, [features["left_eye"]], (0, 255, 0))
	image = ffdet.draw_features(image, [features["right_eye"]], (0, 0, 255))
	face = features["face"]
	left_eye = features["left_eye"]
	right_eye = features["right_eye"]
	roi_face = image[face[1]:face[1]+face[3], face[0]:face[0]+face[2]]
	roi_left_eye = image[left_eye[1]:left_eye[1]+left_eye[3], \
				left_eye[0]:left_eye[0]+left_eye[2]]
	roi_right_eye = image[right_eye[1]:right_eye[1]+right_eye[3],\
			right_eye[0]:right_eye[0]+right_eye[2]]
	cv2.imshow("FACE", roi_face)
	cv2.imshow("LEFT_EYE", roi_left_eye)
	cv2.imshow("RIGHT_EYE", roi_right_eye)
else:
	print("no features found!")


plt.imshow(image)
plt.show()