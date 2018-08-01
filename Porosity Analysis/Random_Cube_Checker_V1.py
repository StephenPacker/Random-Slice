import cv2
import glob
import numpy as np
import math
import random


def main():
	DIR = "C:\Users\spack\Desktop\MicroCT\Practice Data\Salt_1_recon"
	files = (glob.glob(DIR + "/*.bmp"))

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file, 0))

	width = images[1].shape[0]
	height = images[1].shape[1]
	center = (int(width // 2), int(height // 2))
	radius = radius_finder(images, width, center)

	cv2.circle(images[0], center, radius, 255)

	cv2.imshow('Visualize Radius', images[0])
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	cube_generator(center, radius, len(images))


# This Method returns a radius such that everything within the circle is of the imaged data (i.e puts a upper limit on
# the boundary of our CT data) ensuring that we dont included any invalid pixels in our datasets.
def radius_finder(images, width, center):
	radii = []

	for i in range(0, len(images), int(math.floor(len(images) // 10))):
		width_index = width
		cur_i = images[i]
		cur_p = cur_i[center[1], width - 1]

		while cur_p == 0 and width_index > 0:
			width_index -= 1
			cur_p = cur_i[center[1], width_index]
		# cur_i[center[1], width_index] = 255 Draws the line showing the loops traversal

		radii.append(width_index - center[0])

	return max(radii)


# Determines whether a pixel (x,y co-ord) is within the range of a circle delimiting the boundary of our data set.
def is_in_circle(center, radius, x, y):
	return np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < radius


def cube_generator(center, radius, stack_height):
	# In future versions, the length of the cube will be based on a REV calculation
	c_len = 100

	lower_2D_bound = (center[0] - radius) + c_len
	upper_2D_bound = center[0] + (radius - c_len)
	upper_3D_bound = stack_height - c_len


	print((upper_2D_bound - lower_2D_bound)**2) * upper_3D_bound # Total # of starting cube locations

	bottom_left_coord = []
	adders = [[0, 0, 0], [0, c_len, 0], [c_len, 0, 0], [c_len, c_len, 0], [0, 0, c_len], [0, c_len, c_len],
	          [c_len, 0, c_len], [c_len, c_len, c_len]]
	vertices = []

	for i in range(2):
		bottom_left_coord.append(random.randrange(lower_2D_bound, upper_2D_bound))

	bottom_left_coord.append(random.randrange(0, upper_3D_bound))

	for i in range(8):
		vertices.append([a+b for a, b in zip(bottom_left_coord, adders[i])])

	print(vertices)


main()
