import cv2
import matplotlib.pyplot as plt
import ffdet

# example
capture = cv2.VideoCapture(0)
facial_features_list, image = ffdet.get_facial_features_from_capture(capture)

if facial_features_list:
	features = facial_features_list[0]
	image_features = image.copy()
	image_features = ffdet.draw_features(image_features, [features["face"]], (255, 0, 0))
	image_features = ffdet.draw_features(image_features, [features["left_eye"]], (0, 255, 0))
	image_features = ffdet.draw_features(image_features, [features["right_eye"]], (0, 0, 255))

	plt.figure()
	plt.imshow(image_features, cmap='gray')

	plt.show()
else:
	print("no features found!")
