# My final goal is to create a stochastic algorithm that generates random 2D sections from a 3D volume
# Later iteration will work on more complex geometries (spheres and cylinders), and be able to take slices from all
# 360 degrees of a 3D volume

# The first prototype deals with 90 slices of a square from the same starting point, by using the same starting point
# I can ensure that all random sections have the same "thickness" thus keeping the data consistent. The first prototype
# only works on 2D arrays simulating a square and is only able to select a 1D array. Additionally, the size of the cube
# and thus the max section width is fixed. Finally, the precision of the algorithm is quite low as I am rounding to the
# first decimal, I dont know how to increase the precision at this time, I do believe this issue will be less apparent
# when dealing with larger data sets.


import math
import random
import numpy as np


def main():

	slope = slope_generator()
	array = array_generator()
	slicer(array, slope)


def array_generator():
	counter = 0
	test_array = np.zeros([10, 10])
	for i in range(len(test_array)):
		for j in range(len(test_array)):
			counter += 1
			test_array[i][j] = counter
	return test_array


def slope_generator():
	angle = random.randrange(1, 90)
	radians = math.radians(angle)
	slope = math.tan(radians)
	print(angle, slope)
	return slope


def slicer(array, slope):
	if slope >= 1:
		slicer_a(array, round(slope))
	else:
		slope = round(1/slope)
		slicer_b(array, slope)


# Currently Slicer A only works for angles greater than 45, the method for angles less than 45 is very similar
# But essentially the opposite so I will handle such a case with Slicer B...
def slicer_a(array, slope):
	max_slice = 10
	position = (max_slice, 0)
	new_slice = []
	while len(new_slice) < max_slice and position[0] - 1 >= 0:
		j = 0
		while abs(position[0] - 1) < max_slice and j < slope and len(new_slice) < max_slice:
			j += 1
			position = (position[0] - 1, position[1])
			new_slice.append(array[position])
		position = (position[0], position[1] + 1)
	print(new_slice)


def slicer_b(array, slope):
	print(slope)
	max_slice = 10
	position = (max_slice - 1, -1)
	new_slice = []
	while len(new_slice) < max_slice and position[1] + 1 < max_slice:
		j = 0
		while position[1] + 1 < max_slice and j < slope and len(new_slice) < max_slice:
			j += 1
			position = (position[0], position[1] + 1)
			new_slice.append(array[position])
		position = (position[0] - 1, position[1])
	print(new_slice)


main()

