from daycare import daycare
from common import inputString, yes
from save import *

def main():
	if yes(input("Load savefile? ")):
		care = loadSave("testsave.json")#load(input("Which savefile do you want to load? "))
	else:
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
