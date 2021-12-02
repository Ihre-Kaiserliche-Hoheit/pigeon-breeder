from common import *
from string import digits, ascii_letters

class pigeonClass:
	def __init__(self, pigeonUID, name, sex, parents:list=None, genes:dict=dict()):
		self.uid = pigeonUID
		self.name = name
		self.age = 0 # Age in months

		self.isFemale = sex
		self.canReproduce = True
		self.isAlive = True
		self.timesBreed = 0

		self.didAct = True

		self.genes = genes
		self.effectiveValues = calcValues(self.genes)
		self.genesSequenced = False

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
		for geneticValueKey in self.effectiveValues:
			geneticValueString += "%s: %s\n"%(geneticValueKey, self.effectiveValues[geneticValueKey])
		return geneticValueString.rstrip().title()

	def returnParentsString(self):
		parents = ""
		if self.parents != None:
			for parent in self.parents:
				parents += str(parent.uid) + ", "
			parents = parents.rstrip(", ")

		return parents if parents != "" else None

	def showGenes(self):
		geneString = ""
		for chromosomeKey in self.genes:
			geneString += self.genes[chromosomeKey]
		return geneString

	def show(self):
		stringyBoi = ("UID: %s \n"%(self.uid) +
			"Name: %s \n"%(self.name) +
			"Age: %s Months \n"%(self.age) +
			"Gender: %s \n"%(self.getGender()) +
			"Alive: %s \n"%(self.isAlive) +
			"Parents: %s"%(self.returnParentsString()) +
			self.returnGeneticValueString())

		return stringyBoi

def calcValues(genes):
	geneValues = dict()
	for geneKey in genes:
		alleles = "".join(sorted(list(genes[geneKey])))

		for allele in alleles:
			lenAlleles = len(set([alleles.lower() for al in alleles]))
			if lenAlleles == 1:
				try:
					geneValues[allele] += 2
				except KeyError:
					geneValues[allele] = 2
				break

			elif lenAlleles == 2:
				try:
					geneValues[alleles[0]] += 1
				except KeyError:
					geneValues[alleles[0]] = 1

	effectiveValues = {
		"speed":0,
		"size":0,
		"fluff":0
	}

	for alleleKey in geneValues:
		match alleleKey:
			case "A" | "a":
				effectiveValues["speed"] += geneValues[alleleKey]

			case "B" | "b":
				effectiveValues["size"] += geneValues[alleleKey]

			case "C" | "c":
				effectiveValues["fluff"] += geneValues[alleleKey]

			case "E" | "e":
				effectiveValues["fluff"] -= geneValues[alleleKey]

			case "F" | "f":
				effectiveValues["size"] -= geneValues[alleleKey]

			case "G" | "g":
				effectiveValues["speed"] -= geneValues[alleleKey]

	for valueKey in effectiveValues:
		if effectiveValues[valueKey] < 0:
			effectiveValues[valueKey] = 0
	return effectiveValues
