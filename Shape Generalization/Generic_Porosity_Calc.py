# This porosity calculator is designed to work with essentially any shape, assuming the scan only has one sample, and
# that the sample is relatively closed (Picture pouring syrup on top of the provided images, if the water flows around
# the image that means the porosity calc should be accurate, if the water flows though the image the accuracy will
# likely be much lower).

import glob
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import random

file_location = None
loop_inc = 1  # Represents the step for the main loop, skips loop_inc - 1 images for faster runtime
width_inc = 1  # Represents the inc/decrementer in shape outliner, bigger number skips more pixels for faster runtime
save_count = 0  # Keeps track of how many comparison images are saved, solely for naming purposes


# Main control for program, reads in images, iterates through images counting porosity via shape_outliner
def main():

	images = file_reader()  # Read in images
	porosities = []

	start = time.time()

	# Iterate through the images and count the porosity
	for i in range(0, len(images), loop_inc):
		print(i)
		total_img_pixels = np.count_nonzero(images[i])
		if total_img_pixels != 0:
			shape = shape_outliner(images[i])
			total_shape_pixels = np.count_nonzero(shape)
			porosities.append(por_calc(total_img_pixels, total_shape_pixels))

	porosities = np.array(porosities)

	end = time.time()
	print("TIME: " + str(end - start))

	print(np.average(porosities))


# Mimics a ROI shrink wrap procedure. Traces across original image until it encounters a white pixel, all the while
# writing black pixels to the shape array. In doing this, it outlines the sample within each image,
# which can then be used to calculate porosity.
def shape_outliner(image):

	height = image.shape[0]
	width = image.shape[1]
	shape = np.ones((height, width), dtype=int)
	cur_i = image

	# Move left to right across image moving down
	for j in range(0, height):
		width_index = width - 1
		height_index = j
		cur_p = cur_i[height_index, width_index]  # Starting in top right corner
		while cur_p == 0 and width_index > width_inc:  # Go until image has white pixel or reach boundary
			width_index -= width_inc
			cur_p = cur_i[height_index, width_index]
		shape[height_index, width_index:width] = 0

	# Move right to left moving down
	for j in range(0, height):
		width_index = 0
		height_index = j
		cur_p = cur_i[height_index, width_index]  # Starting in top left corner
		while cur_p == 0 and width_index < width - width_inc:  # Go until image has white pixel or reach boundary
			width_index += width_inc
			cur_p = cur_i[height_index, width_index]
		shape[height_index, 0:width_index] = 0

	shape = cv2.medianBlur(shape.astype(np.float32), 5)  # Sooth images to remove border irregularities

	# Randomly choose to save a comparison image (Ensure shape outliner works properly)
	if random_saver():
		image_saver(image, shape)

	return shape


def por_calc(bright_pixels, total_pixels):
	return (1 - (bright_pixels/float(total_pixels))) * 100


# Reads in image files specified by the users
def file_reader():
	global file_location

	while True:
		file_location = raw_input("Please specify the file path to where your images are stored: ")
		file_type = raw_input("Please specify the file type. I.e bmp: ")
		files = (glob.glob(file_location + "/*." + file_type))
		images = []
		for img_file in files:
			images.append(cv2.imread(img_file, 0))
		if len(images) == 0:
			print("The folder location or file type you selected were invalid, please try again")
			continue
		break

	return images


# Saves a plot showing a image and its corresponding shape outline, allows user to ensure proper operation of code
def image_saver(image, shape):
	global save_count

	plt.subplot(2, 1, 1)
	plt.imshow(image, cmap="gray")
	plt.subplot(2, 1, 2)
	plt.imshow(shape, cmap="gray")
	plt.savefig(file_location + " Comparison Number " + str(save_count) + ".jpg")
	save_count += 1


# Randomly saves an image based on a user determined probability "odds"
def random_saver():
	odds = 10  # Think of this as probability to save = 1/odds
	x = random.randrange(odds)
	if x == odds - 1:
		return True
	else:
		return False


main()
