# My final goal is to create a stochastic algorithm that generates random 2D sections from a 3D volume
# Later iteration will work on more complex geometries (spheres and cylinders), and be able to take slices from all
# 360 degrees of a 3D volume hopefully by rotating on two axises, possibly using different starting points.

# In the final working version, We can rotate a plane 360 degrees (on one axis) through a 3D cube that simulates
# the porosity of a rock sample. The cube and its porosity can be customized.

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

	increments = slice_prep(slope_angle[1], cube)

	random_slice = slicer(cube, slope_angle[0], increments)
	visualizer(cube, random_slice, slope_angle[1], porosity)


# Rounds down to the nearest ten, used to make sure the starting position of slice generation is appropriate (If we
# were to start in the middle then we have a trailing edge somewhere that fucks up the algorithm)
def round_down(x):

	return int(math.floor(x / 10.0)) * 10


# Generates a cube of user specified dimensions, cubes have to be odd otherwise there is no "true" center line with
# which I can start at.
def cube_generator(cube_dimension, porosity):

	cube = []

	# Determine the dimensions of a cube and step (step determines how dense points will be)
	max_x = max_y = max_z = cube_dimension
	step = 1

	# Creates a cube like structure with customizable parameters
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

	angle = random.randrange(79, 81)
	radians = math.radians(angle)
	slope = math.tan(radians)
	slope_angle = [slope, angle]

	return slope_angle


# Prepares the slicing algorithm for proper operation based on the slope given previously, this method allows the slicer
# to be slightly more generic, and thus reduces a lot of redundant code.
def slice_prep(angle, cube):

	cube_root = int((len(cube)**(1./3.)) + 1)

	if 0 < angle <= 45:
		inner_indexer = cube_root
		outer_indexer = cube_root**2

	elif 45 < angle <= 90:
		inner_indexer = cube_root**2
		outer_indexer = cube_root

	elif 90 < angle <= 135:
		inner_indexer = cube_root**2
		outer_indexer = -cube_root

	else:
		inner_indexer = -cube_root
		outer_indexer = cube_root**2

	increments = [inner_indexer, outer_indexer]

	return increments


# The guts of the program, the slicer generates the slices we see in the figure based upon a given slope. it includes 2
# sets of nested while loops which slice in the positive and negative direction respectively, starting from the center.
#
# Although the while loops are nested, they don't run in O(n^2) because both loops have a nearly identical stopping
# condition and once the inner loop stops the outer loop will stop closely after. Still, this is likely the bottleneck
# Of the analysis especially with two for loops at the end.
def slicer(cube, slope, incrementer):

	if abs(slope) < 1:
		slope = round(1/slope)
	else:
		slope = round(slope)

	cube_root = int((len(cube)**(1./3.)) + 1)
	max_slice = ((cube_root ** 2) // 2) + 1
	position = round_down((len(cube)//2) + 1)
	inner_increment = incrementer[0]
	outer_increment = incrementer[1]
	new_slice = []
	inverse_new_slice = []

	slope_incrementer = False
	counter = 0

	# Move to the right of the origin
	while len(new_slice) < max_slice:
		j = 0
		counter += 1
		if counter > 1:
			slope_incrementer = True
		while j < abs(slope) and len(new_slice) < max_slice:
			j += 1
			for i in range(cube_root):
				new_slice.append(cube[position + i])
			position += inner_increment
		position += outer_increment

	position = (round_down((len(cube) // 2) + 1))
	position = position - inner_increment

	if slope_incrementer:
		position = position - outer_increment

	counter = 0

	# Move to the left of the origin
	while len(inverse_new_slice) < (max_slice - cube_root):
		counter += 1
		if counter > 1 or slope_incrementer:
			j = 0
		while j < abs(slope) and len(inverse_new_slice) < (max_slice - cube_root):
			j += 1
			for i in range(cube_root):
				inverse_new_slice.append(cube[position + i])
			position -= inner_increment
		position -= outer_increment

	# Combine the two old slices
	master_slice = []
	for i in range(len(new_slice)):
		master_slice.append(new_slice[i])
	for j in range(len(inverse_new_slice)):
		master_slice.append(inverse_new_slice[j])

	return master_slice


# Visualizes the cube and random cube slice along with pertinent information
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

	custom_scale = len(random_slice)/10

	ax.set_zlim(0, custom_scale)

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

	plt.legend(loc='lower right')

	plt.show()


main()
