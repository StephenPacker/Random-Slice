import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math
import random

# Having a very hard time generating a sphere, looks much more like a diamond... not exactly sure how I can improve
# without using more sophisticated methods
sphere = []


def main():

	print("Greetings, This simple program allows a user to generate a simple 3D 'sphere' and fill it with porosity")

	radius = input("Please enter a radius for the sphere: ")
	step = 1
	horizontal_step = 0
	horizontal_max = False

	# Nasty looking for loop handles the creation of a spherical shape, could use refinement but as a crude analog it
	# Should suffice until I start looking at some real data
	for i in range(0, radius + 1, step):
		if not horizontal_max:
			horizontal_step += 1
		else:
			horizontal_step -= 1
		if horizontal_step >= radius // 2:
			horizontal_max = True
		bottom_sphere_section_generator(step, radius, i, horizontal_step)
		top_sphere_section_generator(step, radius, i, horizontal_step)

	porosity = input("Please Enter a Porosity Percentage: ")
	if porosity > 1:
		porosity = porosity / 100

	volume = len(sphere)

	porosity_generator(porosity, volume)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	# A very crude loop whose purpose is to determine if each point is a 1 indicating solid, or 0 indicating void
	# Ideally I will color code these points based on this value to map porosity! (i.e probably will have to split into
	# Two separate data sets).

	solid = []
	pore = []

	for j in range(len(sphere)):
		if sphere[j][3] == 1:
			solid.append(sphere[j])
		else:
			pore.append(sphere[j])

	solid_volume = np.array(solid)
	pore_volume = np.array(pore)

	# Make a quick check to ensure that some porosity/solid exists so we dont encounter an index error
	if len(solid) >= 1:
		ax.scatter(solid_volume[:, 0], solid_volume[:, 1], solid_volume[:, 2], color='blue', label='Solid')
	if len(pore) >= 1:
		ax.scatter(pore_volume[:, 0], pore_volume[:, 1], pore_volume[:, 2], color='red', label='Pore Space')

	plt.legend(loc='upper left')
	plt.show()

	ax.set_xbound(-(radius-6), radius-6)

	plt.show()


# Similar code as 3D volume generator prototype 3 except this time im looking to generate sections of a sphere instead
# of a cube
def bottom_sphere_section_generator(step, radius, height, horizontal_step):
	shrinking_circle = radius
	for i in range(1, horizontal_step + 1, step):
		shrinking_circle -= 2
		for j in range(-shrinking_circle, shrinking_circle, step):
			sphere.append([i, j, height, 1])


def top_sphere_section_generator(step, radius, height, horizontal_step):
	shrinking_circle = radius
	for i in range(0, -horizontal_step, -step):
		shrinking_circle -= 2
		for j in range(-shrinking_circle, shrinking_circle, step):
			sphere.append([i, j, height, 1])


def porosity_generator(percentage, volume):
	needed_cells = int(math.ceil(volume * percentage))
	indices = random.sample(range(len(sphere)), needed_cells)
	for i in range(len(indices)):
		sphere[indices[i]][3] = 0


main()