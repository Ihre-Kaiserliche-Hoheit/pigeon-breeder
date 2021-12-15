from random import randint
from json import load

class Species:
	def __init__(self, name:str, canBreed:bool, averageLifeExpectancy:int, childLower:int, childUpper:int, fertility:int):
		self.name = name # Name of species
		self.averageLifeExpectancy = averageLifeExpectancy # How old they get on average
		self.canBreed = canBreed
		self.childLower = childLower # How many children they have at minimum
		self.childUpper = childUpper # How many children they have at maximum
		self.fertility = fertility # How likely they are to reproduce

	def childCount(self):
		return randint(self.childLower, self.childUpper)

def generateSpecies():
	data = load(open("../input/species.json"))
	outputDict = dict()

	for species in data:
		outputDict[species] = Species(data[species]["name"], data[species]["canBreed"], data[species]["averageLifeExpectancy"], data[species]["childLower"], data[species]["childUpper"], data[species]["fertility"])
		
	return outputDict