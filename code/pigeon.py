from common import *
from creature import *

class Pigeon(Creature):
	def __init__(self, name, isFemale, parents:list=None, genes:dict=dict()):
		self.UID = len(self.allCreatures)
		self.name = name
		self.age = 0 # Age in months

		self.isFemale = isFemale
		self.canReproduce = True
		self.isAlive = True

		self.didAct = True

		self.genes = genes
		self.genesSequenced = False

		self.price = 0

		self.parents = parents # Dictionary of all parents
		self.children = dict() # Dictionary of all children

	def getGender(self):
		return "Female" if self.isFemale else "Male"

	def show(self):
		showString = ("UID: %s \n"%(self.UID) +
			"Name: %s \n"%(self.name) +
			"Age: %s Months \n"%(self.age) +
			"Gender: %s \n"%(self.getGender()) +
			"Alive: %s \n"%(self.isAlive) +
			"Parents: %s"%(self.returnParentsString()))

		return showString
