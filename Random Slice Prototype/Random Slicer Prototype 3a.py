# My final goal is to create a stochastic algorithm that generates random 2D sections from a 3D volume
# Later iteration will work on more complex geometries (spheres and cylinders), and be able to take slices from all
# 360 degrees of a 3D volume

# Taking a step back from prototype 4, It was a bad idea to try and work from the corners, It makes much more sense to
# Just try and use a 'center' point (Which should exist on a odd sized cube....) and that way the angles actually make
# logical sense.

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
	visualizer(random_slice)


def cube_generator():

	cube = []

	# Determine the dimensions of a cube and step (step determines how dense points will be)
	max_x = 9
	max_y = 9
	max_z = 9
	step = 1

	# Might try and use I to make cube center the origin, could make things easier to work with
	i = max_x//2

	counter = 0

	# Creates a cube like structure with customizable parameters
	for z in range(0, max_z, step):
		for x in range(0, max_x, step):
			for y in range(0, max_y, step):
				counter += 1
				cube.append([x, y, z, counter])

	return cube


def slope_generator():

	angle = random.randrange(1, 180)
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


def visualizer(random_slice):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	random_slice = np.array(random_slice)

	ax.scatter(random_slice[:, 0], random_slice[:, 1], random_slice[:, 2])

	ax.set_ybound(-2, 10)
	ax.set_xbound(-2, 10)
	ax.set_zlim(0, 10)

	ax.set_xlabel("X_Axis")
	ax.set_ylabel("Y_Axis")
	ax.set_zlabel("Z_Axis")

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
		inner_indexer = cube_root
		outer_indexer = -cube_root**2

	else:
		inner_indexer = -(cube_root**2)
		outer_indexer = cube_root


	incrementers = [inner_indexer, outer_indexer]

	return incrementers


main()
