# Im just going to keep the data in the format provided by glob, it works well enough so lets not fuck with it too much!

import cv2
import glob
import numpy as np


def main():

	DIR = "C:\Users\spack\Documents\Summer Research Code\Image Pre Processing\Test_Data"
	files = (glob.glob(DIR + "/*.bmp"))

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file))

	print(type(images[0]))

	# width = images[1].shape[0]
	# height = images[1].shape[1]
	#
	# img_stack = np.ndarray
	#
	# for i in range(0, len(images)):
	# 	for j in range(0, width):
	# 		for k in range(0, height):
	# 			img_stack[i][j][k] = images[i][j][k]

	cv2.imshow('First Image', images[0])
	cv2.waitKey(0)
	cv2.destroyAllWindows()


main()
