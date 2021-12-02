from daycare import daycare
from common import inputString
from save import *

def main():
	care = daycare(input("How do you want to call your pigeon care?\n"), "../input/pigeonNames.json", "../input/help.txt")
	care.do("help")

	while True:
		try:
			if care.do(input(inputString())) == 0:
				save(care)
				break
		except EOFError:
				save(care)
				print("\n")
				break
		except IndexError:
			continue

main()
