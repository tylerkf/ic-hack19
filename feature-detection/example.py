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
else:
	print("no features found!")

plt.imshow(image)
plt.show()