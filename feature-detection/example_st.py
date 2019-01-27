# run: python example_st.py --shape-predictor shape_predictor_68_face_landmarks.dat
import cv2
import matplotlib.pyplot as plt
import ffdet_st as ffdet
import detect_blinks as blinky

# example
capture = cv2.VideoCapture(0)
facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

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
0
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

plt.imshow(image)
plt.show()


# if left_EAR < EYE_AR_THRESH and right_EAR > EYE_AR_THRESH:
# 	return -1
# elif left_EAR > EYE_AR_THRESH and right_EAR < EYE_AR_THRESH:
# 	return 1
# else:
# 	return 0



