cube = []

# Determine the dimensions of a cube and step (step determines how dense points will be)
max_x = 9
max_y = 9
max_z = 9
step = 1

counter = 0

# Creates a cube like structure with customizable parameters
for z in range(0, max_z, step):
	for x in range(0, max_x, step):
		for y in range(0, max_y, step):
			cube.append([x, y, z, counter])
			counter += 1

print(cube[((9*9*9)//2)+1])
