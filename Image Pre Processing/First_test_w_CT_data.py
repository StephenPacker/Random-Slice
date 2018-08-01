import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

def main():

	img = cv2.imread('Salt_17.0um_2k_rec0034.bmp', 0)

	plt.subplot(1, 2, 1)
	plt.imshow(img, cmap='gray')

	plt.subplot(1, 2, 2)

	binary_img = quick_segment(img)
	plt.imshow(binary_img, cmap='gray')

	plt.show()


def quick_segment(img):
	porosity = 0.0
	img2 = img.copy()
	for i in range(0, img.shape[0]):
		for j in range(0, img.shape[1]):
			if img2[i][j] <= 2:
				img2[i][j] = 0
			if img2[i][j] == 0:
				porosity += 1
	print(porosity/(img.shape[0] * img.shape[1]))

	return img2

main()