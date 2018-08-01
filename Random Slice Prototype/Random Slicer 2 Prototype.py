# My final goal is to create a stochastic algorithm that generates random 2D sections from a 3D volume
# Later iteration will work on more complex geometries (spheres and cylinders), and be able to take slices from all
# 360 degrees of a 3D volume hopefully by rotating on two axises, possibly using different starting points.

# I am now trying a new version of the random slice algorithm... the older version did work but was highly buggy and
# really only worked for 9*9*9 cubes... additionally, by implementing this updated implementation of the slicing
# algorithm I could hypothetically begin doing the slicing in two different directions and starting at points not going
# through the center of the cube

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import random


# The main function delegates the various method calls in the program and also deals with all user input
def main():
	porosity = input("Please enter a porosity percentage or type r to generate a random porosity: ")
	if porosity == 'r' or porosity == 'R':
		porosity = (float(random.uniform(0.0, 100.0)) / 100)
	if porosity > 1:
		porosity = (float(porosity) / 100)

	cube_dimension = input("Please enter a dimension for a side of the cube: ")
	if cube_dimension % 2 == 0:
		cube_dimension = cube_dimension - 1

	cube = cube_generator(cube_dimension, porosity)
	slope_angle = slope_generator()
	increment = slice_prep(slope_angle[1], cube)

	random_slice = slice_plane(positions_plane(cube, slope_angle[1]), cube, increment, slope_angle[0])

	visualizer(cube, random_slice, slope_angle[1], porosity)


# Rounds down to the divisible numeral, used to make sure the starting position of slice/plane generation is appropriate
def round_down(x, cube):
	starting_position = x

	cube_dimension = int((len(cube) ** (1. / 3.)) + 1)

	while starting_position % cube_dimension != 0:
		starting_position -= 1

	return starting_position


# Generates a cube of user specified dimensions, cubes have to be odd otherwise there is no "true" center line with
# which I can start at.
def cube_generator(cube_dimension, porosity):
	cube = []

	# Determine the dimensions of a cube and step (step determines how dense points will be)
	max_x = max_y = max_z = cube_dimension
	step = 1

	# Creates a cube represented as a 1d array of "4D points" i.e each point has an x,y,z value and a fourth value
	# Indicating if it is solid(1) or porous(0). This way of representing a 3D volume is essential to my random slice
	# Algorithm, if I were to adapt this methodology to a real 3D volume It would first need to be preprocessed into a
	# 1D array which could be really slow... likely meaning It will need modifications when translating to ct data
	for z in range(0, max_z, step):
		for x in range(0, max_x, step):
			for y in range(0, max_y, step):
				cube.append([x, y, z, 1])

	volume = max_z * max_x * max_y

	porosity_generator(porosity, volume, cube)

	return cube


# Fills the cube with porosity in a completely random fashion, the amount of porosity can be user determined or random
def porosity_generator(percentage, volume, cube):
	needed_cells = int(math.ceil(volume * percentage))
	indices = random.sample(range(len(cube)), needed_cells)
	for i in range(len(indices)):
		cube[indices[i]][3] = 0


# Generates an angle and slope with which we will use to slice our cube
def slope_generator():
	angle = random.randrange(89, 91)
	radians = math.radians(angle)
	slope = math.tan(radians)

	if abs(slope) < 1:
		slope = round(1 / slope)
	else:
		slope = round(slope)

	slope_angle = [abs(slope), angle]

	return slope_angle


# Prepares the slicing algorithm for proper operation based on the slope given previously, this method allows the slicer
# to be slightly more generic, and thus reduces a lot of redundant code.
def slice_prep(angle, cube):
	cube_root = int((len(cube) ** (1. / 3.)) + 1)

	if 0 < angle <= 45:
		increment = cube_root ** 2

	elif 45 < angle <= 90:
		increment = cube_root

	elif 90 < angle <= 135:
		increment = -cube_root

	else:
		increment = - cube_root ** 2

	return increment


# Generates either a vertical or horizontal plane that we will manipulate with a given slope to represent a random slice
# This plane is actually a 1D array of positions, each position represents a pixel location in the 3D volume
def positions_plane(cube, angle):
	plane = []

	cube_dimension = int((len(cube) ** (1. / 3.)) + 1)

	plane_size = cube_dimension ** 2

	if 0 < angle <= 45 or 135 < angle <= 180:
		position = round_down((len(cube) // 2) + 1, cube)

		# Starting at the center point fill the plane array with all positions in said plane in a horizontal pattern,
		# Need to correct for python starting at zero and not 1
		for i in range(((-plane_size // 2) + 1) + position + int(position / cube_dimension ** 2),
		               ((plane_size // 2) + 1) + position + int(position / cube_dimension ** 2)):
			plane.append(i)

	elif 45 < angle <= 90 or 90 < angle <= 135:
		position = round_down((plane_size // 2) + 1, cube)

		# Starting at the center point fill the plane array with all positions in said plane in a vertical pattern
		for i in range(cube_dimension):
			for j in range(cube_dimension):
				plane.append(position + j + (i * plane_size))

	return plane


# Manipulates the plane generated in positions plane based upon an angle, this mimics a random slice through a cube
# And is much more stable and readable then the previous version which is very nice.
def slice_plane(plane, cube, increment, slope):
	random_slice = []
	cube_root = int(math.sqrt(len(plane)))
	position = round_down(len(plane) // 2, cube) + 1

	j = cube_root
	incrementer = 0

	for i in range(position + cube_root - 1, cube_root ** 2):
		if j >= (slope * cube_root):
			incrementer += increment
			j = 0
		j += 1
		plane[i] = plane[i] + incrementer

	incrementer = 0

	for i in range(position - 2, -1, -1):
		if j >= (slope * cube_root):
			incrementer += increment
			j = 0
		plane[i] = plane[i] - incrementer
		j += 1

	for i in range(len(plane)):
		random_slice.append(cube[plane[i]])

	return random_slice


def porosity_counter(random_slice):

	counter = 0

	for i in range(len(random_slice)):
		if random_slice[i][3] == 0:
			counter += 1.0

	return (counter/len(random_slice)) * 100


# Visualizes the cube and random cube slice along with pertinent information... The method of showing porosity is really
# Slow and could definitely be improved upon in later iterations
def visualizer(cube, random_slice, angle, porosity):
	fig = plt.figure(1)
	ax = fig.add_subplot(111, projection='3d')

	ax.set_xlabel("X_Axis")
	ax.set_ylabel("Y_Axis")
	ax.set_zlabel("Z_Axis")

	plt.title("Cube with " + str("{0:.2f}".format(porosity * 100)) + "% porosity")

	solid = []
	pore = []

	for j in range(len(cube)):
		if cube[j][3] == 1:
			solid.append(cube[j])
		else:
			pore.append(cube[j])

	solid_volume = np.array(solid)
	pore_volume = np.array(pore)

	# Make a quick check to ensure that some porosity/solid exists so we don't encounter an index error
	if len(solid) >= 1:
		ax.scatter(solid_volume[:, 0], solid_volume[:, 1], solid_volume[:, 2], color='blue', label='Solid')
	if len(pore) >= 1:
		ax.scatter(pore_volume[:, 0], pore_volume[:, 1], pore_volume[:, 2], color='red', label='Pore Space')

	plt.legend(loc='lower right')

	fig = plt.figure(2)
	ax = fig.add_subplot(111, projection='3d')

	ax.set_xlabel("X_Axis")
	ax.set_ylabel("Y_Axis")
	ax.set_zlabel("Z_Axis")

	plt.title(str(angle) + " degree slice through cube with " + str("{0:.2f}".format(porosity * 100)) + "% porosity")

	solid = []
	pore = []

	for j in range(len(random_slice)):
		if random_slice[j][3] == 1:
			solid.append(random_slice[j])
		else:
			pore.append(random_slice[j])

	solid_volume = np.array(solid)
	pore_volume = np.array(pore)

	# Make a quick check to ensure that some porosity/solid exists so we don't encounter an index error
	if len(solid) >= 1:
		ax.scatter(solid_volume[:, 0], solid_volume[:, 1], solid_volume[:, 2], color='blue', label='Solid')
	if len(pore) >= 1:
		ax.scatter(pore_volume[:, 0], pore_volume[:, 1], pore_volume[:, 2], color='red', label='Pore Space')

	ax.scatter([], [], [], color='white',
	           label="This random slice has " + str("{0:.2f}".format(porosity_counter(random_slice))) + "% porosity")

	plt.legend(loc='lower right')

	plt.show()


main()
