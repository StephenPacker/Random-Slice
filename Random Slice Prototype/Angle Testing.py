import math

angle = 0
radians = math.radians(angle)
slope = math.tan(radians)

if abs(slope) < 1:
	slope = round(1 / slope)
else:
	slope = round(slope)

print(slope)
