from random import choice
from json import load

class Genetics:
	# Initilize genetics
	genetics = load(open("../input/genetics.json"))

	# Shared variables, all iterations of the class will be affected should they be changed
	validMutations = genetics["possibleMutations"]
	validGenes = genetics["possibleGenes"]
	geneBlocks = genetics["geneBlocks"]

	del genetics

	def __init__(self, genes:dict=dict()):
		self.genes = genes

	def getRandomGeneticHalf(self):
		# Returns a dict containing a randomly selected half of the current genes
		halfGenes = dict()

		for alleleKey in self.genes:
			halfGenes[alleleKey] = choice(self.genes[alleleKey])

		return halfGenes

	def countGenes(self):
		# Returns a dict containing a count of all unique alleles present in the genes dict
		counterDict = dict()

		for alleleKey in self.genes:
			key = "".join(sorted(list(self.genes[alleleKey]))) # Sorts the string by turning it into a list and back into a string

			try:
				counterDict[key] += 1
			except KeyError:
				counterDict[key] = 1

		return counterDict

	def mutation(self):
		# Randomly mutates one allele
		key = choice(list(self.genes.keys()))
		gene = list(self.genes[key])
		allele = choice(gene)

		mutation = choice(self.validMutations[allele])

		for i in range(len(gene)):
			if gene[i] == allele:
				gene[i] = mutation
				self.genes[key] = "".join(gene)

				break

	def geneString(self):
		# Returns a continues string from self.genes
		geneString = ""

		for chromosomeKey in self.genes:
			geneString += self.genes[chromosomeKey]

		return geneString
