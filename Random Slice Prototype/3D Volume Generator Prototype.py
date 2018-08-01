from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


def main():
	figure = plt.figure()
	ax = figure.add_subplot(111, projection='3d')

	array = [1,2,3,4,5]

	X = array
	Y = array
	Z = array

	ax.plot(X, Y, Z)

	plt.show()


main()
