import cv2
import glob
import numpy as np
import math


def main():

	DIR = "C:\Users\spack\Desktop\MicroCT\Practice Data\Salt_1_recon"
	files = (glob.glob(DIR + "/*.bmp"))

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file))

	width = images[1].shape[0]
	height = images[1].shape[1]
	center = (int(width // 2), int(height // 2))

	cv2.circle(images[0], center, radius_finder(images), (0, 0, 255))

	cv2.imshow('Visualize Radius', images[0])
	cv2.waitKey(0)
	cv2.destroyAllWindows()


# This Method returns a radius such that everything within the circle is of the imaged data (i.e puts a upper limit on
# the boundary of our CT data) ensuring that we dont included any invalid pixels in our datasets.
def radius_finder(images):

	radii = []

	width = images[1].shape[0]
	height = images[1].shape[1]
	center = [int(width//2), int(height//2)]

	for i in range(0, len(images), int(math.floor(len(images)//10))):
		width_index = width
		cur_i = images[i]
		cur_p = cur_i[center[1], width - 1, 0]

		while cur_p == 0 and width_index > 0:
			width_index -= 1
			cur_p = cur_i[center[1], width_index, 0]
			cur_i[center[1], width_index, 0] = 255

		radii.append(width_index - center[0])

	return min(radii)


main()
