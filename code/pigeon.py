from common import *
import textwrap as tw

class pigeonClass:
	def __init__(self, pigeonUID, name, sex, parents:list=None):
		self.uid = pigeonUID
		self.name = name
		self.age = 0 # Age in months

		self.isFemale = sex
		self.canReproduce = True
		self.isAlive = True
		self.timesBreed = 0

		self.didAct = True

		self.genetics = {
			"fluff":1,
			"speed":1,
			"size":1
		}

		self.parents = parents
		self.children = dict() #Dictionary of all children

	def addChild(self, child):
		#Adds child where needed
		self.children[str(child.uid)] = child

	def getGender(self):
		return "Female" if self.isFemale else "Male"

	def anyGeneticValueOneOrLess(self):
		for geneticValueKey in self.genetics.keys():
			if self.genetics[geneticValueKey] <= 1:
				return True

	def returnEmptyGenetics(self):
		genetics = dict()
		for geneticKey in self.genetics.keys():
			genetics[geneticKey] = 0
		return genetics

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

	def show(self):
		stringyBoi = ("UID: %s \n"%(self.uid) +
			"Name: %s \n"%(self.name) +
			"Age: %s Months \n"%(self.age) +
			"Gender: %s \n"%(self.getGender()) +
			"Alive: %s \n"%(self.isAlive) +
			"Parents: %s"%(self.returnParentsString()) +
			self.returnGeneticValueString())

		return tw.dedent(stringyBoi)
