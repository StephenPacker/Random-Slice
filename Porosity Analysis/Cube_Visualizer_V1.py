import cv2
import glob
import numpy as np
import math
import random
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


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

	# Will be based on some sort of REV calculation in the future
	c_len = 10

	vertex = vertex_generator(center, radius, c_len)
	plane = plane_slicer(vertex, images, c_len)
	values = cube_slicer(vertex, images, c_len, len(images))
	cube = values[0]
	z_position = values[1]
	ax = make_ax(True)

	cv2.circle(images[z_position], center, radius, 255)

	#facecolors = plt.get_cmap('Greys')
	ax.voxels(cube, edgecolors='gray')
	plt.show()

	plt.subplot(1, 2, 1)
	plt.title("CT Image with dataset border")
	plt.imshow(images[z_position], cmap='gray')

	plt.subplot(1, 2, 2)
	plt.title("Square starting at x: %i, y: %i" % (vertex[0], vertex[1]))
	plt.imshow(plane, cmap='gray')

	plt.show()


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
def is_in_circle(center, radius, verticies):
	print("Test")
	for i in range(0, len(verticies)):
		if np.sqrt((verticies[i][0] - center[0]) ** 2 + (verticies[i][1] - center[1]) ** 2) > radius:
			return False
	return True

# Generates a Vertex and checks to make sure all points of a cube emanating from said vertex fit inside out dataset.
# Right now it "Just Works" but there is a much cleaner way to execute this loop.
def vertex_generator(center, radius, c_len):

	lower_2D_bound = center[0] - radius
	upper_2D_bound = center[0] + radius

	vertices = []
	bottom_left_coord = []
	adders = [[0, 0], [0, c_len], [c_len, 0], [c_len, c_len]]

	for i in range(2):
		bottom_left_coord.append(random.randrange(lower_2D_bound, upper_2D_bound))
	for i in range(4):
		vertices.append([a + b for a, b in zip(bottom_left_coord, adders[i])])

	while not is_in_circle(center, radius, vertices):
		vertices = []
		bottom_left_coord = []
		for i in range(2):
			bottom_left_coord.append(random.randrange(lower_2D_bound, upper_2D_bound))
		for i in range(4):
			vertices.append([a + b for a, b in zip(bottom_left_coord, adders[i])])
		is_in_circle(center, radius, vertices)

	return vertices[0]

# Generates a plane given a vertex
def plane_slicer(vertex, images, c_len):

	plane = np.zeros([c_len, c_len], int)
	i = 0

	for x in range(vertex[0], vertex[0] + c_len - 1):
		i += 1
		j = 0
		for y in range(vertex[1], vertex[1] + c_len - 1):
			j += 1
			plane[i][j] = images[0][x][y]

	return plane


# Generates a cube given a vertex, I NEED TO CLEAN UP THESE INDICES
def cube_slicer(vertex, images, c_len, stack_height):

	upper_3D_bound = stack_height - c_len
	z_position = random.randrange(0, upper_3D_bound)

	cube = np.zeros([c_len, c_len, c_len], int)
	k = -1

	for z in range(z_position, z_position + c_len):
		k += 1
		i = 0
		for x in range(vertex[0], vertex[0] + c_len - 1):
			i += 1
			j = 0
			for y in range(vertex[1], vertex[1] + c_len - 1):
				j += 1
				cube[i][j][k] = images[z][x][y]

	values = (cube, z_position)

	return values


def make_ax(grid=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.grid(grid)
    return ax

main()
