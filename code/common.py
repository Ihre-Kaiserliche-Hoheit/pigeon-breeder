from sys import platform
from os import system
from random import randint

"""
Shared Functions
"""
def isNotEmpty(List):
	# Returns False if empty and True if not empty
	return bool(len(List))

def isEmpty(List):
	# Returns the opposit of isNotEmpty
	return not isNotEmpty(List)

def inputString():
	return "\nWhat do you do? "

def whatOS():
	# Returns which OS is used
	return platform

def clearCMD():
	# Clears commandline
	system('"clear"')

def random3D6():
	# Returns a 3d6 result
	result = 0

	for i in range(3):
		result += randint(1, 6) # This gives a nice bell curve

	return result

def curve(a:float, x:float, d:float, e:float):
	return a * (x-d)**2 + e

def yes(value):
	value = str(value).lower()
	match value:
		case "yes" | "ye" | "y" | "oi":
			return True
		case _:
			return False

def abort(value):
	value = str(value).lower()
	match value:
		case "abort" | "a":
			return True
		case _:
			return False
