import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

points = np.array([[-1, -1, -1, 1],
                  [1, -1, -1, 1],
                  [1, 1, -1, 1],
                  [-1, 1, -1, 1],
                  [-1, -1, 1, 1],
                  [1, -1, 1, 1],
                  [1, 1, 1, 1],
                  [-1, 1, 1, 1]])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(len(points)):
	if points[i][3] == 1:
		print('test')

ax.scatter(points[:, 0], points[:, 1], points[:, 2])

plt.show()
