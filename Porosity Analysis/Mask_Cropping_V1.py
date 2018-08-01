import cv2
import glob
import numpy as np


def main():

	DIR = "C:\Users\spack\Documents\Summer Research Code\Image Pre Processing\Test_Data"
	files = (glob.glob(DIR + "/*.bmp"))

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file))

	width = images[1].shape[0]
	height = images[1].shape[1]

	center = [int(width//2), int(height//2)]

	cv2.imshow('First Image', images[0])
	cv2.waitKey(0)
	cv2.destroyAllWindows()


# Determines whether a pixel (x,y co-ord) is within the range of a circle delimiting the boundary of our data set.
# This method will be used to ensure all vertices of a cube lie within the dataset, ensuring that only relevant pixels
# Are counted.
def is_in_circle(center, radius, x, y):

	return np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2) < radius


main()
