import cv2
import matplotlib.pyplot as plt
import ffdet
from detect_blinks import eye_aspect_ratio as EAR

# example
capture = cv2.VideoCapture(0)
facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

if facial_features_list:
	features = facial_features_list[0]
	image = ffdet.draw_features(image, [features["face"]], (255, 0, 0))
	image = ffdet.draw_features(image, [features["left_eye"]], (0, 255, 0))
	image = ffdet.draw_features(image, [features["right_eye"]], (0, 0, 255))
	face_xy = features["face"]
	left_eye_xy = features["left_eye"]
	right_eye_xy = features["right_eye"]
	face = image[face_xy[1]:face_xy[1]+face_xy[3], \
				face_xy[0]:face_xy[0]+face_xy[2]]
	left_eye = image[left_eye_xy[1]:left_eye_xy[1]+left_eye_xy[3], \
				left_eye_xy[0]:left_eye_xy[0]+left_eye_xy[2]]
	right_eye = image[right_eye_xy[1]:right_eye_xy[1]+right_eye_xy[3],\
			right_eye_xy[0]:right_eye_xy[0]+right_eye_xy[2]]
	cv2.imshow("FACE", face)
	cv2.imshow("LEFT_EYE", left_eye)
	cv2.imshow("RIGHT_EYE", right_eye)
else:
	print("no features found!")

plt.imshow(image)
plt.show()

EYE_AR_THRESH = 0.3

left_EAR = EAR(left_eye)
right_EAR = EAR(right_eye)

print(left_EAR)
print(right_EAR)

# if left_EAR < EYE_AR_THRESH and right_EAR > EYE_AR_THRESH:
# 	return -1
# elif left_EAR > EYE_AR_THRESH and right_EAR < EYE_AR_THRESH:
# 	return 1
# else:
# 	return 0



