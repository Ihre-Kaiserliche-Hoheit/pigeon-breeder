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

	def getRandomName(self, sex:str):
		return choice(self.randomNames[sex.lower()]) # Returns random name

	def createCreature(self, name, isFemale, parents:list=None, genes:dict=dict()):
		newCreature = Pigeon(name, isFemale, parents, genes)
		newCreature.birth()

		return newCreature

	def calcCost(self, pigeonValues):
		pass

	def buyCreature(self):
		pass

	def sellCreature(self, UID):
		# Code to sell pigeons goes here
		if not self.isValidPigeon(UID):
			print("Pigeon not found or dead, try another pigeon")
			return None

		values = self.pigeons[UID].effectiveValues
		values["age"] = self.pigeons[UID].age
		price = int(round(self.calcCost(values) * 0.95))
		confirmation = input("You can sell the pigeon for %s do you accept? ((Yes(y)/No(n)) "%(price))

		if yes(confirmation):
			self.death(self.pigeons[UID])
			self.wealth += price
			print("Pigeon sold!")

		else:
			print("Okay, then not")

	def genetics(self, parents:list):
		genes = parents[0].geneBlocks

		for parent in parents:
			for gene in genes:
				genes[gene] += parent.genes[gene]

		return genes

	def reproduce(self, parents:list, numberOfChildren:int):
		for i in range(numberOfChildren):
			UID = self.getUID()
			genes = self.genetics(parents)
			child = self.createCreature("Pigeon " + str(UID), bool(getrandbits(1)), parents, genes)

			if self.deathConditions(child):
				self.death(child)

			for parent in parents: # Supports more than two parents!
				parent.addChild(child)

	def breed(self, parents):
		modifier = 0 # Modifies the propability of reproduction, pigeons that breed the first time should get a modifier = 2
		alwaysSucceed = isDebugOn # Left in for potential future uses

		for parent in parents:
			parent.didAct = True

		if randint(0, 100) < self.breedingDifficulty * modifier or alwaysSucceed == True:
			self.reproduce(parents, 2)

			return 0

		return 1

	def death(self, pigeon):
		del self.pigeons[str(pigeon.UID)]
		pigeon.isAlive = False

	def update(self):
		self.month += 1
		livingPigeons = self.pigeons

		for pigeonKey in livingPigeons:
			pigeon = livingPigeons[pigeonKey]
			pigeon.age += 1
			pigeon.didAct = False

			if self.deathConditions(pigeon) and randint(0, 100) < 20:
				self.death(pigeon)

		print(self.info())

	def info(self):
		infoString = ("\nDaycare Name: " + self.name + "\n" +
		"Month: " + str(self.month))
		infoString += "\nPigeons:"
		if isNotEmpty(self.pigeons):
			infoString += "\n"

			for pigeonKey in self.pigeons:
				pigeon = self.pigeons[pigeonKey]
				infoString += ("UID: %s; Name: %s; Gender: %s; DidAct: %s\n"%(pigeon.UID, pigeon.name, pigeon.getGender(), pigeon.didAct))
		else:
			infoString += "\nNone"

		return infoString.rstrip()

	def renamePigeon(self, UID, name):
		if not self.isValidPigeon(UID):
			print("Pigeon not found or dead, try another pigeon")
			return None

		if name == "r":
			name = self.getRandomName(self.livingCreatures[str(UID)].getGender())

		self.livingCreatures[UID].name = name

	def isValidPigeon(self, UID):
		# Check if the given UID is a valid living pigeon
		try:
			self.livingCreatures[UID]
			return True

		except KeyError:
			return False

	def didActList(self):
		# Returns a list of pigeons that didn't act
		lopta = list() # lopta -> listOfPigeonsThatActed

		for pigeonKey in self.pigeons:
			pigeon = self.pigeons[pigeonKey]
			if pigeon.didAct == True:
				lopta.append(pigeon)
		return lopta

	def didNotActList(self):
		# Returns a list of pigeons that did act
		lopthna = list() # lopthna -> listOfPigeonsThatHaveNotActed

		for pigeonKey in self.pigeons:
			pigeon = self.pigeons[pigeonKey]
			if pigeon.didAct == False:
				lopthna.append(pigeon)
		return lopthna

	def deathConditions(self, target):
		if 72 < target.age:
			return True
		return False

	def breedCommand(self, UID1:int, UID2:int):
		try:
			pigeons = [self.pigeons[UID1], self.pigeons[UID2]]
		except KeyError:
			print("You picked one or more pigeons that don't exist!")
			return 0

		female = None
		male = None

		for pigeon in pigeons:
			if pigeon.isFemale == True and female == None and pigeon.didAct == False:
				female = pigeon
				continue
			elif pigeon.isFemale == False and male == None and pigeon.didAct == False:
				male = pigeon
				continue
			else:
				print("You picked two pigeons of the same gender!")
				return 0

		if self.breed([male, female]) == 0:
			print("Success!")
		else:
			print("Failure")

	def renamePigeonCare(self, newName:str):
		self.name = newName

	def commandHelp(self):
		print(self.help.rstrip())

	def do(self, command):
		command = command.lower().split()

		match command[0]:
			# Replace this with dynamic funtion calls
			case "breed":
				if isEmpty(self.didNotActList()):
					print("There are no pigeons left that can breed this month, either end this month or do something else.")
					return None
				self.breedCommand(command[1], command[2])

			case "info":
				print(self.info())

			case "show":
				try:
					print(self.allPigeons[str(command[1])].show())
				except KeyError:
					print("Pigeon not found")
				except IndexError:
					print("Pigeon not found")

			case "buy":
				self.buyCreature()

			case "sell":
				self.sellCreature(command[1])

			case "genetics":
				try:
					print(self.pigeons[command[1]].geneString())
				except KeyError:
					print("Pigeon not found")
				except IndexError:
					print("Pigeon not found")

			case "kill":
				pass # ToDo: Add way for player to activly kill pigeons

			case "rename":
				self.renamePigeon(command[1], command[2])

			case "pass":
				self.update()

			case "help" | "h" | "?":
				self.commandHelp()

			case "clear":
				clearCMD()

			case "quit" | "q":
				return 0

			case "save":
				save(self)
				print("Saved!")

			case _:
				print("Command Not Found")
