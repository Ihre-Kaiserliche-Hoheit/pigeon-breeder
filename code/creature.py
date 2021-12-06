from genetics import *

class Creature(Genetics):
	livingCreatures = dict()
	allCreatures = dict()

	def __init__(self, UID, isFemale:bool, species:any, genes:dict, parents:list=list(), isAlive:bool=True):
		self.UID = UID

		self.species = species

		self.genes = genes
		self.age = 0

		self.parents = parents
		self.children = list()

		self.isAlive = isAlive
		self.isFemale = isFemale
		self.canReproduce = species.canBreed

		self.didAct = True

	def addChildren(self, children:list=list(), parents:list=list()):
		parents.append(self) # Makes sure self is always in the list
		parents = list(set(parents)) # Removes duplicates from the list
		children = list(set(children)) # Same as above but for children

		for parent in parents:
			parent.children = children

	def returnParentsAsString(self):
		parentString = ""

		for parentUID in self.parents:
			parentString += str(parentUID) + ", "
		parentString = parentString.rstrip(", ")

		return parentString # If no parents exist for the creature returns an empty string

	def getGender(self):
		# Converts self.isFemale into a string that either says female or male
		return "female" if self.isFemale else "male"

	def birth(self):
		self.allCreatures[self.UID] = self
		self.livingCreatures[self.UID] = self

	def death(self):
		self.isAlive = False
		del self.livingCreatures[self.UID]
