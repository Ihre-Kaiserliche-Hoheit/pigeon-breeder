from genetics import *

class Creature(Genetics):
    livingCreatures = dict()
    allCreatures = dict()

    def __init__(self, UID, genes:dict, parents:dict=dict(), isAlive:bool=True:
        self.UID = UID

        self.genes = genes

        self.parents = parents
        self.children = dict()

        self.isAlive = isAlive

    def addChild(self, children:list=list(), parents:list=list()):
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

    def returnGeneString(self):
        geneString = ""

        for geneKey in self.genes:
            geneString += self.genes[geneKey]

    def countAlleles(self):
        alleleCount = dict()

        for geneKey in self.genes:
            alleles = "".join(sorted(list(self.genes[geneKey])))

    		for allele in alleles:
    			lenAlleles = len(set([al.lower() for al in alleles])) # What is this doing?
    			if lenAlleles == 1:
    				try:
    					alleleCount[allele] += 2
    				except KeyError:
    					alleleCount[allele] = 2
    				break # Jumps to next loop as all alleles were counted

    			elif lenAlleles == 2:
    				try:
    					alleleCount[alleles[0]] += 1
    				except KeyError:
    					alleleCount[alleles[0]] = 1

        return alleleCount # Returns always a dict, but may sometimes be empty
