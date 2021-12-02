from pigeon import *
from common import *
from save import *
from random import getrandbits, randint, choice, choices
import textwrap as tw
from json import load

class daycare:
	def __init__(self, name, randomNameFilePath:str, helpFilePath:str):
		self.name = name

		self.month = 1 # Time is given in months

		self.wealth = 50

		self.pigeons = dict()
		self.allPigeons = dict()

		self.breedingDifficulty = 25 #the n out of 100 chance to successfully reproduce

		self.randomNames = load(open(randomNameFilePath, "r"))
		self.help = open(helpFilePath, "r").read()
		self.genes = {
			"chromosome0":"",
			"chromosome1":"",
			"chromosome2":"",
			"chromosome3":"",
			"chromosome4":"",
			"chromosome5":"",
			"chromosome6":"",
			"chromosome7":"",
			"chromosome8":"",
			"chromosome9":"",
			"chromosome10":"",
			"chromosome11":"",
			"chromosome12":"",
			"chromosome13":"",
			"chromosome14":"",
			"chromosome15":"",
			"chromosome16":"",
			"chromosome17":"",
			"chromosome18":"",
			"chromosome19":"",
			"chromosome20":""
		}
		self.geneValues = ["fluff", "speed", "size"]
		self.alleles = "ABCDEFGabcdefg"

	def getPigeonUID(self):
		return len(self.allPigeons) # Returns a UID for the most recent pigeon

	def getRandomName(self, sex:str):
		return choice(self.randomNames[sex.lower()]) # Returns random name

	def createPigeon(self, pigeonUID, name, isFemale, parents:list=None, genes:dict=dict()):
		newPigeon = pigeonClass(pigeonUID, name, isFemale, parents, genes)
		self.allPigeons[str(newPigeon.uid)] = newPigeon
		self.pigeons[str(newPigeon.uid)] = newPigeon

		return newPigeon

	def calcCost(self, pigeonValues):
		# Calculates the value of the pigeon
		cost = 1

		for value in self.geneValues:
			cost += pigeonValues[value] * 0.5
		cost = cost * curve(-0.9, (pigeonValues["age"]/36), 1, 1) # 36 = Median Age

		return int(round(cost, 0))

	def buyPigeon(self):
		while True:
			data = {
				"age":randint(6, 72),
				"female":bool(getrandbits(1))
			}
			genetics = dict()

			for gene in self.genes:
				genetics[gene] = "".join(choices(self.alleles, k=2))

			geneValues = calcValues(genetics)

			data = data | geneValues

			data["cost"] = self.calcCost(data)
			infoString = "Age: %s Months\nGender: %s\nCost: %s\n"%(data["age"], "Female" if data["female"] else "Male", data["cost"])
			for value in geneValues:
				infoString += "%s: %s\n"%(value.title(), data[value])
			print(infoString)

			confirmation = input("Do you want to buy the pigeon?(Yes(y)/No(n)/Abort(a)) ")

			if yes(confirmation):
				if self.wealth < data["cost"]:
					print("You have not enought money to buy this pigeon!")
					confirmation = input("Do you want to look for another pigeon(Yes(y)/No(n)) ")

					if not yes(confirmation):
						break
					continue

				uid = self.getPigeonUID()
				pigeon = self.createPigeon(uid, "Pigeon " + str(uid), data["female"], genes=genetics)
				self.renamePigeon(str(uid), "r")
				pigeon.age = data["age"]

				break

			elif abort(confirmation):
				break

			else:
				continue

	def sellPigeon(self, pigeonUID):
		#Code to sell pigeons goes here
		if not self.isValidPigeon(pigeonUID):
			print("Pigeon not found or dead, try another pigeon")
			return None

		values = self.pigeons[pigeonUID].effectiveValues
		values["age"] = self.pigeons[pigeonUID].age
		price = int(round(self.calcCost(values) * 0.95))
		confirmation = input("You can sell the pigeon for " + str(price) + ", do you accept? ((Yes(y)/No(n)) ")

		if yes(confirmation):
			self.death(self.pigeons[pigeonUID])
			self.wealth += price
			print("Pigeon sold!")

		else:
			print("Okay, then not")

	def genetics(self, parents:list):
		genes = self.genes

		for parent in parents: # Picks one allele per parent
			for geneKey in parent.genes:
				genes[geneKey] += choice(parent.genes[geneKey]) # Picks random allele from parent

		return genes

	def reproduce(self, parents:list, numberOfChildren:int):
		for i in range(numberOfChildren):
			pigeonUID = self.getPigeonUID()
			genes = self.genetics(parents)
			child = self.createPigeon(pigeonUID, "Pigeon " + str(pigeonUID), bool(getrandbits(1)), parents, genes)

			if self.deathConditions(child):
				self.death(child)

			for parent in parents: # Supports more than two parents!
				parent.addChild(child)
				parent.timesBreed += 1

	def breed(self, parents):
		timesBreed = [parent.timesBreed for parent in parents]
		modifier = 0 # Modifies the propability of reproduction, pigeons that breed the first time should get a modifier = 2
		alwaysSucceed = True # Left in for potential future uses

		for value in timesBreed:
			if value == 0:
				modifier += 1
				break
			modifier += 1 / value

		for pigeon in parents:
			pigeon.didAct = True

		if randint(0, 100) < self.breedingDifficulty * modifier or alwaysSucceed == True:
			self.reproduce(parents, 2)

			return 0

		return 1

	def death(self, pigeon):
		del self.pigeons[str(pigeon.uid)]
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
				infoString += ("UID: %s; Name: %s; Gender: %s; DidAct: %s\n"%(pigeon.uid, pigeon.name, pigeon.getGender(), pigeon.didAct))
		else:
			infoString += "\nNone"

		return infoString.rstrip()

	def renamePigeon(self, pigeonUID, name):
		if not self.isValidPigeon(pigeonUID):
			print("Pigeon not found or dead, try another pigeon")
			return None

		if name == "r":
			name = self.getRandomName(self.pigeons[str(pigeonUID)].getGender())

		self.pigeons[str(pigeonUID)].name = name

	def isValidPigeon(self, pigeonUID):
		# Check if the given uid is a valid pigeon
		try:
			self.pigeons[str(pigeonUID)]
			return True

		except KeyError:
			return False

	def didActList(self):
		# Returns a list of pigeons that didn't act
		lopta = list() #lopta -> listOfPigeonsThatActed

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

	def deathConditions(self, pigeon):
		if 72 < pigeon.age:
			return True
		return False

	def breedCommand(self, pigeonUID1:int, pigeonUID2:int):
		try:
			pigeons = [self.pigeons[pigeonUID1], self.pigeons[pigeonUID2]]
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
				self.buyPigeon()

			case "sell":
				self.sellPigeon(command[1])

			case "genetics":
				try:
					print(self.pigeons[command[1]].showGenes())
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
