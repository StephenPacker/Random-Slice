# The first working prototype to fulfill my summer NSERC. This prototype has the ability to read in a series of recon.
# CT images, find a dataset boundary, generate random cubes within the boundary, and slice the cubes at 0, 45, and 90
# degree angles allowing for visualization and porosity measurements, which are then exported to an excel sheet.

import cv2
import glob
import numpy as np
import math
import random
import xlwt
import matplotlib.pyplot as plt

wb = xlwt.Workbook()
ws = wb.add_sheet("Random Slice Data")


# Main reads in and stores the image files and gets info on there dimensions (used to find data boundary)
# Controls the number of cubic sections the program will generate.
def main():

	# This code block removes any hard coding from main.

	# file_location = raw_input("Please specify the file path to where your images are stored: ")
	# file_type = raw_input("Please specify file type. I.e .bmp: ")
	# number_of_cycles = raw_input("How many cycles do you wish to do: ")
	# files = (glob.glob(file_location + "/*" + file_type))

	# Default values used for testing

	location = "C:\Users\spack\Desktop\MicroCT\Practice Data\Salt_1_recon"
	files = (glob.glob(location + "/*.bmp"))
	number_of_cycles = 20

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file, 0))

	width = images[1].shape[0]
	height = images[1].shape[1]
	center = (int(width // 2), int(height // 2))
	radius = radius_finder(images, width, center)

	rev_finder(images, radius, center)

	# Will be based on some sort of REV calculation in the future
	c_len = rev_finder(images, radius, center)

	for i in range(0, number_of_cycles):
		vertex = vertex_generator(center, radius, c_len)
		data = cube_generator(vertex, images, c_len, len(images))
		slices = cube_slicer(data[0], c_len, vertex, data[1])
		# visualizer(images, data[1], slices, center, radius, c_len)


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


# Generates a cube given a vertex (COULD USE SOME TESTING)
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
				cube[z2 - z1][x2 - x1][y2 - y1] = images[z2][y2][x2]

	data = [cube, z_position]

	return data


# This method takes in a ODD SIZED cube and mimics what a sliced plane through its volume would look like. Still a work
# In progress, needs to implement the remainder system to increase accuracy, modify to work with angles between 90-180
# And hopefully streamline the code to reduce redundancies of which there are a few.
def cube_slicer(cube, c_len, vertex, z_position):

	porosities = []
	slices = []

	slice_plane = np.zeros([c_len**2])  # Try with a 1D array and then reshape it. Maybe easier?
	mid_point = ((c_len**2)/2) - (((c_len**2)/2)//c_len)  # Middle of a 1D array of length n*n
	mid_indices = mid_point/c_len  # Middle of a 1D array of length n i.e an x,y,z array in 3D space

	for i in range(mid_point, mid_point + c_len):
		slice_plane[i] = cube[mid_indices][i - mid_point][mid_indices]  # Fill middle of plane with cubes values.

	slope = [0, 1, c_len]  # Mimic a 0, 45, 90 degree angle pairing
	angle = [0, 45, 90]

	current_increment = 1  # Since we already filled the middle row.

	for i in range(0, len(slope)):
		slice_plane = right_slice_builder(cube, slice_plane, current_increment, slope[i], mid_point + c_len, mid_indices)
		slice_plane = left_slice_builder(cube, slice_plane, current_increment, slope[i], mid_point, mid_indices)

		slice_plane_copy = list(slice_plane)
		slices.append(slice_plane_copy)

		porosities.append(slice_analyzer(slice_plane))

	data_writer(porosities, vertex, z_position, angle)

	return slices  # Will be used for visualization


# Builds the right side of a slice plane
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


# Builds the left side of a slice plane
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


# Returns the porosity (non-zero pixels/ zero pixels) of a slice plane
def slice_analyzer(slice_plane):

	grain_space = np.count_nonzero(slice_plane)
	return(1 - (grain_space/float(len(slice_plane)))) * 100


# Writes the porosity data to an excel file for further analysis
def data_writer(porosities, vertex, z_position, angle, counter=[0]):

	counter[0] += 1

	# If its the first time opening the sheet, write the angle information on the top row
	if counter[0] == 1:
		ws.write(0, 0, "Angle")
		for i in range(1, len(angle) + 1):
			ws.write(0, i, angle[i - 1])

	ws.write(counter[0], 0, "Slice at (%i,%i,%i)" % (vertex[0], vertex[1], z_position))
	for i in range(1, len(porosities) + 1):
		ws.write(counter[0], i, porosities[i - 1])

	wb.save("Random_Slice_Data.xls")


# Visualizes the middle section of a cube, followed by three angled sections.
def visualizer(images, z_position, slices, center, radius, c_len):

	angle = [0, 45, 90]

	cv2.circle(images[z_position + c_len/2], center, radius, 255)

	plt.subplot(2, 2, 1)
	plt.title("CT Image with circular border")
	plt.imshow(images[z_position + c_len/2], cmap='gray')

	for i in range(0, len(slices)):
		plt.subplot(2, 2, i + 2)
		plt.title("Slice at %i degrees" % angle[i])
		np.reshape(slices[i], [c_len, c_len])
		plt.imshow(np.reshape(slices[i], [c_len, c_len]), cmap='gray')

	plt.show()


# Returns a approximate REV which I will use as the length of my cubes. Based on a line growing algorithm, which is
# rooted in the assumption that a 1D REV will translate in a 3D system, which will work for homogeneous samples only.
def rev_finder(images, radius, center):

	total_nonzero_pix = 0

	# Currently, I am going to implement the quick and dirty approach. It will be more accurate to go through each
	# pixel and turn it black before doing non-zero counts, however, this also could probably be done
	# much faster in Step 2 (Image Pre-Processing, something that needs more work). A very slow procedure.

	# for z in range(0, len(images)):
	# 	for x in range(0, images[0].shape[0]):
	# 		for y in range(0, images[0].shape[1]):
	# 			if np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) > radius:
	# 				images[z][y][x] = 0

	# Count total porosity for the data set
	for i in range(0, len(images)):
		total_nonzero_pix += np.count_nonzero(images[i])

	volume = math.pi * (radius ** 2) * i
	total_porosity = por_calc(total_nonzero_pix, volume)

	# Grow a line until it contains a similar porosity to the total i.e a line of REV

	line_holder = []

	for j in range(0, 1000):
		random_image = random.randrange(0, len(images))

		line = [images[random_image][center[0]][center[1]]]
		gi = 0  # Growth Incrementer

		while por_calc(np.count_nonzero(line), len(line)) < total_porosity - 1 or\
			por_calc(np.count_nonzero(line), len(line)) > total_porosity + 1 and gi < center[0] - 1:

			gi += 1
			line.extend([images[random_image][center[0] - gi][center[1] - gi]])
			line.extend([images[random_image][center[0] + gi][center[1] + gi]])

		line_holder.append(len(line))

	return sum(line_holder) / len(line_holder)


def por_calc(bright_pixels, total_pixels):
	return (1 - (bright_pixels/float(total_pixels))) * 100


main()
