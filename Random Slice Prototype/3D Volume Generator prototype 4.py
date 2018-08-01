# The exact same as Prototype #3 except this time I am going to try and generate some random heterogeneity

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
import math

# Current solution requires volume to be a global variable, this keeps us from making volume an array of arrays
# which was initially hampering me from proper plotting
cube = []


def main():

	# Determine the dimensions of a cube and step (step determines how dense points will be)
	max_x = 10
	max_y = 10
	max_z = 10
	step = 1

	volume = max_x * max_y * max_z

	# Creates a cube like structure with customizable parameters
	for i in range(0, max_z, step):
		section_generator(step, max_x, max_y, i)

	porosity_generator(1, volume)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# A very crude loop whose purpose is to determine if each point is a 1 indicating solid, or 0 indicating void
	# Ideally I will color code these points based on this value to map porosity! (i.e probably will have to split into
	# Two separate data sets).

	solid = []
	pore = []

	for j in range(len(cube)):
		if cube[j][3] == 1:
			solid.append(cube[j])
		else:
			pore.append(cube[j])

	solid_volume = np.array(solid)
	pore_volume = np.array(pore)

	# Make a quick check to ensure that some porosity/solid exists so we dont encounter an index error
	if len(solid) >= 1:
		ax.scatter(solid_volume[:, 0], solid_volume[:, 1], solid_volume[:, 2], color='blue')
	if len(pore) >= 1:
		ax.scatter(pore_volume[:, 0], pore_volume[:, 1], pore_volume[:, 2], color='red')

	plt.show()


# This method is going to be hilariously slow, there is probably a better way to do this... I will call this function
# to generate a 2d section of a 3d volume which will be added to the total cube for plotting.
def section_generator(step, max_x, max_y, z):
	for i in range(0, max_x, step):
		for j in range(0, max_y, step):
			cube.append([i, j, z, 1])


def porosity_generator(percentage, volume):
	needed_cells = int(math.ceil(volume * percentage))
	indices = random.sample(range(len(cube)), needed_cells)
	for i in range(len(indices)):
		cube[indices[i]][3] = 0


main()
