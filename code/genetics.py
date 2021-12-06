from random import choice

class genetics:
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
