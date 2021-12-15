from creature import *
from common import *
from species import *
from save import *
from random import getrandbits, randint, choice, choices
from json import load

class daycare:
	def __init__(self, name, randomNameFilePath:str, helpFilePath:str):
		self.name = name

		self.month = 1 # Time is given in months

		self.wealth = 50

		self.isDebugOn = True

		self.species = dict()

		self.breedingDifficulty = 25 # The n out of 100 chance to successfully reproduce

		self.randomNames = load(open(randomNameFilePath, "r"))
		self.help = open(helpFilePath, "r").read()
		self.genes = load(open("../input/genetics.json"))["geneBlocks"]
		self.geneValues = ["fluff", "speed", "size"]
		self.alleles = load(open("../input/genetics.json"))["possibleGenes"]
