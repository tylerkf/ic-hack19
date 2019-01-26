import cv2
import eye

# example
capture = cv2.VideoCapture(0)
facial_features_list = eye.get_facial_features_from_capture(capture, image)

if facial_features_list:
	features = facial_features_list[0]
	image = eye.draw_features(image, [features["face"]], (255, 0, 0))
	image = eye.draw_features(image, [features["left_eye"]], (0, 255, 0))
	image = eye.draw_features(image, [features["right_eye"]], (0, 0, 255))
else:
	print("no features found!")

plt.imshow(image)
plt.show()