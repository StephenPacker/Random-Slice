import glob
import cv2
import numpy as np
import math


def main():

	location = "C:\Users\spack\Desktop\MicroCT\Practice Data\Salt_1_recon"
	files = (glob.glob(location + "/*.bmp"))

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file, 0))

	width = images[1].shape[0]
	height = images[1].shape[1]
	center = (int(width // 2), int(height // 2))

	radii = []

	for i in range(0, len(images), int(math.floor(len(images) // 10))):
		width_index = width
		cur_i = images[i]
		cur_p = cur_i[center[1], width - 1]

		while cur_p == 0 and width_index > 0:
			width_index -= 1
			cur_p = cur_i[center[1], width_index]
		radii.append(width_index - center[0])

	radius = max(radii)

	total_nonzero_pix = 0

	for i in range(0, len(images)):
		total_nonzero_pix += np.count_nonzero(images[i])

	volume = math.pi * (radius ** 2) * i
	total_porosity = por_calc(total_nonzero_pix, volume)
	print(total_porosity)


def por_calc(bright_pixels, total_pixels):
	return (1 - (bright_pixels/float(total_pixels))) * 100

main()