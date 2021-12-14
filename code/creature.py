from genetics import *

class Creature(Genetics):
    livingCreatures = dict()
    allCreatures = dict()

    def __init__(self, UID, genes:dict, parents:dict=dict(), isAlive:bool=True):
        self.UID = UID

        self.genes = genes

        self.parents = parents
        self.children = dict()

        self.isAlive = isAlive

    def addChildren(self, children:list=list(), parents:list=list()):
        parents.append(self) # Makes sure self is always in the list
        parents = list(set(parents)) # Removes duplicates from the list
        children = list(set(children)) # Same as above but for children

        for parent in parents:
            for child in children:
                parent.children[child.UID] = child

    def returnParentsAsString(self):
		parentString = ""

		for parentUID in self.parents:
			parentString += str(parentUID) + ", "
		parentString = parentString.rstrip(", ")

		return parentString # If no parents exist for the creature returns an empty string

	def birth(self):
		self.allCreatures[self.UID] = self
		self.livingCreatures[self.UID] = self

	def death(self):
		self.isAlive = False
		del self.livingCreatures[self.UID]
