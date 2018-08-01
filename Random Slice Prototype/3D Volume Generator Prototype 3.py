# Based on code taken from https://stackoverflow.com/questions/44881885/python-draw-3d-cube on May 17th, 2018

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Current solution requires volume to be a global variable, this keeps us from making volume an array of arrays
# which was initially hampering me from proper plotting
volume = []


def main():

	# Determine the dimensions of a cube and step (step determines how dense points will be)
	max_x = 10
	max_y = 10
	max_z = 10
	step = 1

	# Creates a cube like structure with customizable parameters
	for i in range(0, max_z + 1, step):
		section_generator(step, max_x, max_y, i)

	print(volume)

	plotting_volume = np.array(volume)

	print(plotting_volume)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(plotting_volume[:, 0], plotting_volume[:, 1], plotting_volume[:, 2])

	plt.show()


# This method is going to be hilariously slow, there is probably a better way to do this... I will call this function
# to generate a 2d section of a 3d volume which will be added to the total cube for plotting.
def section_generator(step, max_x, max_y, z):
	for i in range(0, max_x + 1, step):
		for j in range(0, max_y + 1, step):
			volume.append([i, j, z, 1])


main()
