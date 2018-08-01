# My final goal is to create a stochastic algorithm that generates random 2D sections from a 3D volume
# Later iteration will work on more complex geometries (spheres and cylinders), and be able to take slices from all
# 360 degrees of a 3D volume

# In prototype 3a I finally got the pseudo 360 degree coverage of a cubic shape to work although the code is pretty ugly
# And the precision is not very good... Alas, it should provide a good base model for the more sophistic algorithms
# I am hoping to produce when working with the micro CT data. In this, the final prototype, I will add porosity to the
# Cube and have each slice calculate the porosity ratio.

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import random


def main():

	cube = cube_generator()
	values = slope_generator()

	increments = slice_prep(values[1], cube)

	random_slice = slicer(cube, values[0], increments)
	visualizer(random_slice, values[1])


def cube_generator():

	cube = []

	# Determine the dimensions of a cube and step (step determines how dense points will be)
	max_x = 9
	max_y = 9
	max_z = 9
	step = 1

	# porosity = input("Please enter a porosity percentage or type r to generate a random porosity: ")
	# if porosity == 'r' or porosity == 'R':
	# 	porosity = (float(random.randrange(100)) / 100)
	# if porosity > 1:
	# 	porosity = (float(porosity) / 100)

	porosity = 0.5

	# Creates a cube like structure with customizable parameters
	for z in range(0, max_z, step):
		for x in range(0, max_x, step):
			for y in range(0, max_y, step):
				cube.append([x, y, z, 1])

	volume = max_z * max_x * max_y

	cube = porosity_generator(porosity, volume, cube)

	return cube


def porosity_generator(percentage, volume, cube):
	needed_cells = int(math.ceil(volume * percentage))
	indices = random.sample(range(len(cube)), needed_cells)
	for i in range(len(indices)):
		cube[indices[i]][3] = 0
	return cube


def slope_generator():

	angle = random.randrange(90, 180)
	radians = math.radians(angle)
	slope = math.tan(radians)
	print(angle, slope)
	values = [slope, angle]

	return values


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

	master_slice = []
	for i in range(len(new_slice)):
		master_slice.append(new_slice[i])
	for j in range(len(inverse_new_slice)):
		master_slice.append(inverse_new_slice[j])

	return master_slice


def visualizer(random_slice, angle):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	random_slice = np.array(random_slice)

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

	ax.set_ybound(-2, 10)
	ax.set_xbound(-2, 10)
	ax.set_zlim(0, 10)

	ax.set_xlabel("X_Axis")
	ax.set_ylabel("Y_Axis")
	ax.set_zlabel("Z_Axis")

	plt.title(str(angle) + " degree slice through cube with x porosity")

	plt.legend(loc='lower right')
	plt.show()


def round_down(x):

	return int(math.floor(x / 10.0)) * 10


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

	incrementers = [inner_indexer, outer_indexer]

	return incrementers


main()
