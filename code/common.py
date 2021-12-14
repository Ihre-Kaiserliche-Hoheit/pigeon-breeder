from sys import platform
from os import system
from random import randint
from math import pi, e

"""
Shared Functions
"""
def isNotEmpty(List):
	return bool(len(List))

def isEmpty(List):
	return not isNotEmpty(List)

def clearCMD():
	system('"clear"')

def random3D6():
	result = 0
	for i in range(3):
		result += randint(1, 6) # This gives a nice bell curve
	return result

def bellCurve(x:float, a:float=10, b:float=0):
	# a determins highest point, b determins off set, x is x
	return  (a**3) / ((x - b)**2 + a ** 2) # Returns a float

def yes(value):
	value = str(value).lower()

	match value:
		case "yes" | "ye" | "y" | "oi" | "oy" | "ay":
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

def no(value):
	value = str(value).lower()

	match value:
		case "no" | "ne" | "n" | "nope" | "nein" | "nah":
			return True
		case _:
			return False
