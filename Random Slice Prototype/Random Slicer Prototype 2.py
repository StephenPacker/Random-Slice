# My final goal is to create a stochastic algorithm that generates random 2D sections from a 3D volume
# Later iteration will work on more complex geometries (spheres and cylinders), and be able to take slices from all
# 360 degrees of a 3D volume

# In this iteration of my prototype, I will start working with the array representing a 3D cube I generated previously
# In the Cubic Porosity Gen+Visualizer program, I will stick with horizontal and vertical slices on a set dimensions
# Cube. Starting in the middle is causing problems... not really a pure middle point based on how I make the cubes...

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import random


def main():

	cube = cube_generator()
	slope = slope_generator()
	random_slice = slicer(cube, slope)
	visualizer(random_slice)


def cube_generator():

	cube = []

	# Determine the dimensions of a cube and step (step determines how dense points will be)
	max_x = 10
	max_y = 10
	max_z = 10
	step = 1

	counter = 0

	# Creates a cube like structure with customizable parameters
	for z in range(0, max_z, step):
		for x in range(0, max_x, step):
			for y in range(0, max_y, step):
				counter += 1
				cube.append([x, y, z, counter])

	return cube


def slope_generator():
	angle = random.randrange(1, 360)
	radians = math.radians(angle)
	slope = math.tan(radians)
	return slope


def slicer(cube, slope):
	choice = random.sample([True, False], 1)
	if choice[0]:
		random_slice = horizontal_slicer(cube, round(slope))
	else:
		slope = round(1/slope)
		random_slice = vertical_slicer(cube, slope)
	return np.array(random_slice)


def horizontal_slicer(cube, slope):
	max_slice = 200
	left_position = 399
	right_position = 499
	new_slice = []
	while len(new_slice) < max_slice:
		new_slice.append(cube[left_position])
		new_slice.append(cube[right_position])
		left_position -= 1
		right_position -= 1

	print("Horizontal Slice")
	print(new_slice)
	return new_slice


def vertical_slicer(cube, slope):
	max_slice = 200
	left_position = 05
	right_position = 06
	new_slice = []
	while len(new_slice) < max_slice:
		new_slice.append(cube[left_position])
		new_slice.append(cube[right_position])
		left_position += 10
		right_position += 10

	print("Vertical_Slice")
	print(new_slice)
	return new_slice


def visualizer(random_slice):

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(random_slice[:, 0], random_slice[:, 1], random_slice[:, 2])

	ax.set_ybound(-5, 15)
	ax.set_xbound(-5, 15)
	ax.set_zlim(0, 10)

	plt.show()


main()
