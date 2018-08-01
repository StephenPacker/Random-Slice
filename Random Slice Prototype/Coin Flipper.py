import random

def main():
	flips = input("How Many Times do you want to flip a coin: ")
	counter = 0
	i = 0

	while i < flips:
		coin = random.randrange(2)
		if coin == 1:
			counter += 1
		else:
			counter -= 1
		i += 1

	print(counter)


main()
