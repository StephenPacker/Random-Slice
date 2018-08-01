import cv2
import glob
import numpy as np


def main():

	DIR = "C:\Users\spack\Documents\Summer Research Code\Image Pre Processing\Test_Data"
	files = (glob.glob(DIR + "/*.bmp"))

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file))

	width = images[1].shape[0]
	height = images[1].shape[1]

	center = [int(width//2), int(height//2)]

	width_index = width
	cur_i = images[0]
	cur_p = cur_i[center[1], width - 1, 0]

	while cur_p == 0 and width_index > 0:
		width_index -= 1
		cur_p = cur_i[center[1], width_index, 0]
		cur_i[center[1], width_index, 0] = 255

	radius = width_index - center[0]
	print(radius)

	cv2.imshow('Visualize Radius', images[0])
	cv2.waitKey(0)
	cv2.destroyAllWindows()

main()
