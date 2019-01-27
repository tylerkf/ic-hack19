# run: python example_st.py --shape-predictor shape_predictor_68_face_landmarks.dat
import cv2
import matplotlib.pyplot as plt
import ffdet_st as ffdet
import detect_blinks as blinky

# example
capture = cv2.VideoCapture(0)
facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

wink_value, eye_landmarks = blinky.wink_detector(image)
if wink_value == -1:
	print("Ah, you winked with your left eye!")
elif wink_value == 1:
	print("Ah, you winked with your right eye!")
else:
	print("You didn't wink!")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blinky.pupil_detector(gray_image,eye_landmarks)

# Compute and visualize convex hull
# leftEyeHull = cv2.convexHull(eye_landmarks[0])
# rightEyeHull = cv2.convexHull(eye_landmarks[1])
# cv2.drawContours(image, leftEyeHull, -1, (0, 255, 0), 1)
# cv2.drawContours(image, rightEyeHull, -1, (0, 255, 0), 1)
# cv2.imshow("Image", image)

plt.imshow()
plt.show()


# if left_EAR < EYE_AR_THRESH and right_EAR > EYE_AR_THRESH:
# 	return -1
# elif left_EAR > EYE_AR_THRESH and right_EAR < EYE_AR_THRESH:
# 	return 1
# else:
# 	return 0



