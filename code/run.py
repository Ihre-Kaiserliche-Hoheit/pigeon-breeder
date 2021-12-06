# from daycare import daycare
from common import yes
#from save import *
from world import World

def main():
	w = World("Test", "test")
	while True:
		try:
			w.command(input("Input command\n"))
		except EOFError:
			print("End game")
			break

main()
