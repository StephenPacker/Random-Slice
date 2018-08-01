import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Current solution requires volume to be a global variable, this keeps us from making volume an array of arrays
# which was initially hampering me from proper plotting... Having a very hard time generating a sphere, looks much more
# like a diamond... not exactly sure how I can improve without using more sophisticated methods
volume = []


def main():

	radius = 14
	step = 1
	horizontal_step = 0
	horizontal_max = False

	for i in range(0, radius + 1, step):
		if not horizontal_max:
			horizontal_step += 1
		else:
			horizontal_step -= 1
		if horizontal_step >= radius // 2:
			horizontal_max = True
		bottom_sphere_section_generator(step, radius, i, horizontal_step)
		top_sphere_section_generator(step, radius, i, horizontal_step)

	plotting_volume = np.array(volume)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(plotting_volume[:, 0], plotting_volume[:, 1], plotting_volume[:, 2])

	ax.set_xbound(-(radius-6), radius-6)

	plt.show()


# Similar code as 3D volume generator prototype 3 except this time im looking to generate sections of a sphere instead
# of a cube
def bottom_sphere_section_generator(step, radius, height, horizontal_step):
	shrinking_circle = radius
	for i in range(1, horizontal_step + 1, step):
		shrinking_circle -= 2
		for j in range(-shrinking_circle, shrinking_circle, step):
			volume.append([i, j, height, 0])


def top_sphere_section_generator(step, radius, height, horizontal_step):
	shrinking_circle = radius
	for i in range(0, -horizontal_step, -step):
		shrinking_circle -= 2
		for j in range(-shrinking_circle, shrinking_circle, step):
			volume.append([i, j, height, 0])


main()
