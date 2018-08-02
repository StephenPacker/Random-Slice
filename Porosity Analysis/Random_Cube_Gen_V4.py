import cv2
import glob
import numpy as np
import math
import random
import xlwt

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
	c_len = 301

	vertex = vertex_generator(center, radius, c_len)
	cube = cube_generator(vertex, images, c_len, len(images))
	cube_slicer(cube, c_len)


# This Method returns a radius such that everything within the circle is of the imaged data (i.e puts a upper limit on
# the boundary of our CT data) ensuring that we do not included any invalid pixels during future computations.
def radius_finder(images, width, center):

	radii = []

	for i in range(0, len(images), int(math.floor(len(images) // 10))):
		width_index = width
		cur_i = images[i]
		cur_p = cur_i[center[1], width - 1]

		while cur_p == 0 and width_index > 0:
			width_index -= 1
			cur_p = cur_i[center[1], width_index]
		radii.append(width_index - center[0])

	return max(radii)


# Determines whether a pixel (x,y co-ord) is within the range of a circle delimiting the boundary of our data set.
def is_in_circle(center, radius, vertices):

	for i in range(0, len(vertices)):
		if np.sqrt((vertices[i][0] - center[0]) ** 2 + (vertices[i][1] - center[1]) ** 2) > radius:
			return False
	return True


# Generates a Vertex and checks to make sure all points of a cube emanating from said vertex fit inside out data set.
# Right now it "Just Works" but there is a much cleaner way to execute this loop.
def vertex_generator(center, radius, c_len):

	lower_2D_bound = center[0] - radius
	upper_2D_bound = center[0] + radius

	adders = [[0, 0], [0, c_len], [c_len, 0], [c_len, c_len]]

	vertices_in_circle = False

	while not vertices_in_circle:
		vertices = []
		bottom_left_coord = []
		for i in range(2):
			bottom_left_coord.append(random.randrange(lower_2D_bound, upper_2D_bound))
		for i in range(4):
			vertices.append([a + b for a, b in zip(bottom_left_coord, adders[i])])
		vertices_in_circle = is_in_circle(center, radius, vertices)

	return vertices[0]


# Generates a cube given a vertex
def cube_generator(vertex, images, c_len, stack_height):

	upper_3D_bound = stack_height - c_len
	z_position = random.randrange(0, upper_3D_bound)

	cube = np.zeros([c_len, c_len, c_len], int)
	x1 = vertex[0]
	y1 = vertex[1]
	z1 = z_position

	for z2 in range(z_position, z_position + c_len):
		for x2 in range(vertex[0], vertex[0] + c_len):
			for y2 in range(vertex[1], vertex[1] + c_len):
				cube[z2 - z1][x2 - x1][y2 - y1] = images[z2][x2][y2]

	return cube


# This method takes in a ODD SIZED cube and mimics what a sliced plane through its volume would look like.
# Simplest possible execution, just one half of a zero degree plane, no worries about remainders, left and right halves
# Numerous different angles etc.
def cube_slicer(cube, c_len):

	slice_plane = np.zeros([c_len**2])  # Try with a 1D array and then reshape it. Maybe easier?
	mid_point = ((c_len**2)/2) - (((c_len**2)/2)//c_len)  # Middle of a 1D array of length n*n
	mid_indices = mid_point/c_len  # Middle of a 1D array of length n i.e an x,y,z array in 3D space

	for i in range(mid_point, mid_point + c_len):
		slice_plane[i] = cube[mid_indices][i - mid_point][mid_indices]  # Fill middle of plane with cubes values.

	slope = 1

	current_increment = 1  # Since we already filled the middle row.

	slice_plane = right_slice_builder(cube, slice_plane, current_increment, slope, mid_point + c_len, mid_indices)
	slice_plane = left_slice_builder(cube, slice_plane, current_increment, slope, mid_point, mid_indices)

	slice_analyzer(slice_plane)


def right_slice_builder(cube, slice_plane, current_increment, slope, slice_position, mid_indices):

	c_len = len(cube)
	z_position = mid_indices
	x_position = mid_indices

	loop_counter = 0
	max_slice = (c_len - 1) / 2

	while loop_counter < max_slice:
		if current_increment < slope:  # CI measures rows appended before moving horizontally.
			z_position += 1
			current_increment += 1
		else:
			x_position += 1
			current_increment = 0
		for i in range(slice_position, slice_position + c_len):
			slice_plane[i] = cube[z_position][i - slice_position][x_position]
		slice_position += c_len
		loop_counter += 1

	return slice_plane


def left_slice_builder(cube, slice_plane, current_increment, slope, slice_position, mid_indices):

	c_len = len(cube)
	z_position = mid_indices
	x_position = mid_indices

	loop_counter = 0
	max_slice = (c_len - 1) / 2

	while loop_counter < max_slice:
		if current_increment < slope:  # CI measures rows appended before moving horizontally.
			z_position -= 1
			current_increment += 1
		else:
			x_position -= 1
			current_increment = 0
		for i in range(slice_position - c_len, slice_position):
			slice_plane[i] = cube[z_position][i - (slice_position - c_len)][x_position]
		slice_position -= c_len
		loop_counter += 1

	return slice_plane


def slice_analyzer(slice_plane):

	grain_space = np.count_nonzero(slice_plane)
	print(grain_space, len(slice_plane))
	porosity = (1 - (grain_space/float(len(slice_plane)))) * 100

	data_writer(porosity)


def data_writer(porosity):

	wb = xlwt.Workbook()
	ws = wb.add_sheet("First Test Sheet")
	ws.write(0, 0, porosity)
	wb.save("Random_Slice.xls")


# Given an angle, generates a slope
def slope_generator(angle):

	radians = math.radians(angle)
	slope = math.tan(radians)

	return slope


main()
