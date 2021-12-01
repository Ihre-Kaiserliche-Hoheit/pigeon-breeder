from common import *

class pigeonClass:
	def __init__(self, pigeonUID, name, sex, parents:list=None, genes):
		self.uid = pigeonUID
		self.name = name
		self.age = 0 # Age in months

		self.isFemale = sex
		self.canReproduce = True
		self.isAlive = True
		self.timesBreed = 0

		self.didAct = True

		self.genes = genes
		self.effectiveValues = dict()

		self.price = 0

		self.parents = parents
		self.children = dict() #Dictionary of all children

	def addChild(self, child):
		#Adds child where needed
		self.children[str(child.uid)] = child

	def getGender(self):
		return "Female" if self.isFemale else "Male"

	def returnGeneticValueString(self):
		geneticValueString = "\n"
		for geneticValueKey in self.genetics:
			geneticValueString += "%s: %s\n"%(geneticValueKey, self.genetics[geneticValueKey])
		return geneticValueString.rstrip().title()

	def returnParentsString(self):
		parents = ""
		if self.parents != None:
			for parent in self.parents:
				parents += str(parent.uid) + ", "
			parents = parents.rstrip(", ")

		return parents if parents != "" else None

	def calcValues(self):
		price = 0
		for value in self.genetics.keys():
			self.effectiveValues[value] = self.genetics[value]

	def show(self):
		stringyBoi = ("UID: %s \n"%(self.uid) +
			"Name: %s \n"%(self.name) +
			"Age: %s Months \n"%(self.age) +
			"Gender: %s \n"%(self.getGender()) +
			"Alive: %s \n"%(self.isAlive) +
			"Parents: %s"%(self.returnParentsString()) +
			self.returnGeneticValueString())

		return stringyBoi
