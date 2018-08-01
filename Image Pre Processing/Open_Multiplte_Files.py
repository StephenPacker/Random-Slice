import cv2
import glob
import time


def main():

	start = time.time()
	DIR = "C:\Users\spack\Documents\Summer Research Code\Image Pre Processing\Test_Data"
	files = (glob.glob(DIR + "/*.bmp"))

	images = []

	for img_file in files:
		images.append(cv2.imread(img_file))

	end = time.time()
	print(end - start)

	cv2.imshow('First Image', images[0])
	cv2.waitKey(0)
	cv2.destroyAllWindows()


main()
