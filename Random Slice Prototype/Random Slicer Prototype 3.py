# My final goal is to create a stochastic algorithm that generates random 2D sections from a 3D volume
# Later iteration will work on more complex geometries (spheres and cylinders), and be able to take slices from all
# 360 degrees of a 3D volume

# In this iteration of my prototype, I will continue working with the array representing a 3D cube generated previously
# In the Cubic Porosity Gen+Visualizer program. In This iteration, I will try to allow for the 0-90 degree random
# Angles introduced in random slicer #1 and combine it with the slicing method used on random slicer # 2

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
	angle = random.randrange(1, 90)
	radians = math.radians(angle)
	slope = math.tan(radians)
	print(angle, slope)
	return slope


def slicer(cube, slope):
	if slope >= 1:
		random_slice = horizontal_slicer(cube, round(slope))
	else:
		slope = round(1/slope)
		random_slice = vertical_slicer(cube, slope)
	return np.array(random_slice)


def horizontal_slicer(cube, slope):
	max_slice = 100
	position = 0
	new_slice = []
	while len(new_slice) < max_slice:
		j = 0
		while j < slope and len(new_slice) < max_slice:
			j += 1
			for i in range(10):
				new_slice.append(cube[position + i])
			position += 100
		position += 10

	print("Horizontal Slice")
	print(new_slice)
	return new_slice


def vertical_slicer(cube, slope):
	max_slice = 100
	position = 0
	new_slice = []
	while len(new_slice) < max_slice:
		j = 0
		while j < slope and len(new_slice) < max_slice:
			j += 1
			for i in range(10):
				new_slice.append(cube[position + i])
			position += 10
		position += 100

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

	ax.set_xlabel("X_Axis")
	ax.set_ylabel("Y_Axis")
	ax.set_zlabel("Z_Axis")

	plt.show()


main()
