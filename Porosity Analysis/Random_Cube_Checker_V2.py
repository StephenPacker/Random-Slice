import cv2
import glob
import numpy as np
import math
import random
import matplotlib.pyplot as plt


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

	#while True:
	vertex = vertex_generator(center, radius, len(images))
	plane_slicer(vertex, images)


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

# Something here is very wrong!
def vertex_generator(center, radius, stack_height):
	# In future versions, the length of the cube will be based on a REV calculation
	c_len = 200

	lower_2D_bound = (center[0] - radius) + c_len
	upper_2D_bound = center[0] + (radius - c_len)

	vertex = []

	for i in range(2):
		vertex.append(random.randrange(lower_2D_bound, upper_2D_bound))

	return vertex


def plane_slicer(vertex, images):

	c_len = 200
	plane = np.zeros([c_len, c_len], int)
	i = -1

	for x in range(vertex[0], vertex[0] + c_len):
		i += 1
		j = -1
		for y in range(vertex[1], vertex[1] + c_len):
			j += 1
			plane[i][j] = images[0][x][y]

	plt.title("Square starting at x%i, y%i" % (vertex[0], vertex[1]))
	plt.imshow(plane, cmap='gray')
	plt.show()

# def cube_slicer(vertex, c_len, images):
#
# 	upper_3D_bound = len(images) - c_len
# 	z_position = (random.randrange(0, upper_3D_bound))
#
# 	cube = np.array([c_len, c_len, c_len])
#
# 	for z in range (z_position, z_position + c_len):
# 		for x in range(vertex[0], vertex[0] + c_len):
# 			for y in range(vertex[1], vertex[1] + c_len):
# 				cube[x, y, z] = images[z, x, y]


main()
