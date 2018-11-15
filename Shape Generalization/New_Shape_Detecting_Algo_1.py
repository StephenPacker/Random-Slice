import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt


def main():

	location = "C:\Users\spack\Desktop\MicroCT\Practice Data\Mac_Sand\VOI"
	files = (glob.glob(location + "/*.png"))

	# images = []
	#
	# for img_file in files:
	# 	images.append(cv2.imread(img_file, 0))

	# images = cv2.imread('printed_sandstone_8um_4k_rec0068.jpg', 0)  # FOR EASIER TESTING
	shapes = shape_outliner(cv2.imread(files[0], 0))


# Absolutely brute force implementation that transposes the outline or shape of our data set onto a blank array that
# can be referenced as an alternative to assuming all objects are circular in form. Essentially carves the general shape
# Into a new 3D array! If run time is already slow, then fuck it!
def shape_outliner(image):

	height = image.shape[0]
	width = image.shape[1]
	shape = np.ones((height, width), dtype=int)
	cur_i = image

	# Move left to right across the image
	for j in range(0, height):
		width_index = width - 1
		height_index = j
		cur_p = cur_i[height_index, width_index]
		while cur_p == 0 and width_index > 0:
			width_index -= 1
			cur_p = cur_i[height_index, width_index]
			shape[height_index, width_index] = 0

	# Move right to left across the image
	for j in range(0, height):
		width_index = 0
		height_index = j
		cur_p = cur_i[height_index, width_index]
		while cur_p == 0 and width_index < width - 1:
			width_index += 1
			cur_p = cur_i[height_index, width_index]
			shape[height_index, width_index] = 0

	shape = cv2.medianBlur(shape.astype(np.float32), 5)


	plt.title("Regular Image vs Outlined Image")
	plt.subplot(2, 1, 1)
	plt.imshow(image, cmap="gray")
	plt.subplot(2, 1, 2)
	plt.imshow(shape, cmap="gray")
	plt.show()

	return shape


main()
