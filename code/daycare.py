from pigeon import *
from common import *
from random import getrandbits, randint, choice
import textwrap as tw
from json import load

class daycare:
    def __init__(self, name, randomNameFilePath:str, helpFilePath:str):
        self.name = name

        self.month = 1

        self.wealth = 50

        self.pigeons = dict()
        self.allPigeons = dict()

        self.breedingDifficulty = 25 #the n out of 100 chance to successfully reproduce

        self.randomNames = load(open(randomNameFilePath, "r"))
        self.help = open(helpFilePath, "r").read()

    def getPigeonUID(self):
        return len(self.allPigeons) # Returns a UID for the most recent pigeon

    def getRandomName(self, sex:str):
        return choice(self.randomNames[sex.lower()]) # Returns random name

    def createPigeon(self, pigeonUID, name, isFemale, parents:list=None):
        newPigeon = pigeonClass(pigeonUID, name, isFemale, parents)
        self.allPigeons[str(newPigeon.uid)] = newPigeon
        self.pigeons[str(newPigeon.uid)] = newPigeon

        return newPigeon

    def generateRandomPigeon(self):
        randomPigeon = self.createPigeon(self.getPigeonUID(), "Randy", bool(getrandbits(1)))
        randomPigeon.fluffiness = randint(3, 18)
        randomPigeon.speed = randint(3, 18)
        randomPigeon.size = randint(3, 18)

        return randomPigeon

    def buyPigeon(self):
        while True:
            data = {
                "age":randint(6, 72),
                "female":bool(getrandbits(1)),
                "fluff": random3D6(),
                "speed": random3D6(),
                "size": random3D6(),
                "cost":randint(5, 15)
            }

            print(tw.dedent(f"""
                Age: {data["age"]} Months
                Gender: {"Female" if data["female"] else "Male"}
                Cost: {data["cost"]}
                Fluffiness: {data["fluff"]}
                Size: {data["size"]}
                Speed: {data["speed"]}"""))


            confirmation = input("Do you want to buy the pigeon?(Yes(y)/No(n)/Abort(a)) ")
            confirmation = confirmation.lower()

            if confirmation == "n":
                continue

            elif confirmation == "y":
                if self.wealth < data["cost"]:
                    print("You have not enought money to buy this pigeon!")
					#Reuses confirmation variable
                    confirmation = input("Do you want to look for another pigeon(Yes(y)/No(n)) ")
                    if confirmation == "n":
                        break

                    continue

                uid = self.getPigeonUID()
                pigeon = self.createPigeon(uid, "Pigeon " + str(uid), data["female"])
                pigeon.age = data["age"]
                pigeon.fluffiness = data["fluff"]
                pigeon.speed = data["speed"]
                pigeon.size = data["size"]

                break

            else:
                break

    def sellPigeon(self, pigeonUID):
        #Code to sell pigeons goes here
        price = randint(5, 20)
        confirmation = input("You can sell the pigeon for " + str(price) + ", do you accept? ((Yes(y)/No(n))")
        confirmation = confirmation.lower()

        if confirmation == "y":
            self.death(self.pigeons[pigeonUID])
            print("Pigeon sold!")
        else:
            print("Okay, then not")

    def reproduce(self, parents:list, numberOfChildren:int):
        for i in range(numberOfChildren):
            pigeonUID = self.getPigeonUID()
            child = self.createPigeon(uid, "Pigeon " + str(pigeonUID), bool(getrandbits(1)), parents)
            childGenetics = self.genetics(parents)
            child.fluffiness = childGenetics["fluff"]
            child.speed = childGenetics["speed"]
            child.size = childGenetics["size"]
            if self.deathConditions(child):
                self.death(child)

            for parent in parents: #Supports more than two parents!
                parent.addChild(child)
                parent.timesBreed += 1

    def breed(self, male, female):
        timesBreed = [female.timesBreed, male.timesBreed]
        pigeons = [male, female]
        modifier = 0
        alwaysSucceed = False # Left in for potential future uses

        for value in timesBreed:
            if value == 0:
                modifier += 1
                break

            modifier += 1 / value
        for pigeon in pigeons:
            pigeon.didAct = True

        if randint(0, 100) < self.breedingDifficulty * modifier or alwaysSucceed == True:
            self.reproduce(pigeons, 2)

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

    def info(self):
        infoString = ("Daycare Name: " + self.name + "\n" +
        "Month: " + str(self.month))
        infoString += "\nPigeons:"
        if isNotEmpty(self.pigeons):
            infoString += "\n"
            for pigeonKey in self.pigeons.keys():
                pigeon = self.pigeons[pigeonKey]
                infoString += ("UID: %s; Name: %s; Gender: %s; DidAct: %s"%(pigeon.uid, pigeon.name, pigeon.getGender(), pigeon.didAct))
        else:
            infoString += "\nNone"
        return infoString

    def renamePigeon(self, pigeonUID, name):
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

    def genetics(self, parents):
        fluffiness = 0
        speed = 0
        size = 0
        for pigeon in parents:
            fluffiness += pigeon.fluffiness
            speed += pigeon.speed
            size += pigeon.size

        fluffiness = int(fluffiness / len(parents)) + randint(-3, 3)
        speed = int(speed / len(parents)) + randint(-3, 3)
        size = int(size / len(parents)) + randint(-3, 3)

        return {"fluff":fluffiness, "speed":speed, "size":size}

    def deathConditions(self, pigeon):
        if 72 < pigeon.age or pigeon.speed < 1 or pigeon.size < 1 or pigeon.fluffiness < 1:
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

        if self.breed(male, female) == 0:
            print("Success!")
        else:
            print("Failure")

    def renamePigeonCare(self, newName:str):
        self.name = newName

    def do(self, command):
        command = command.lower()

        command = command.split() # Splits command based on whitespaces

        match command[0]:
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

            case "buy":
                self.buyPigeon()

            case "sell":
                if self.isValidPigeon(command[1]):
                    self.sellPigeon(command[1])
                else:
                    print("Pick another pigeon")

            case "kill":
                pass # ToDo: Add way for player to activly kill pigeons

            case "rename":
                if not self.isValidPigeon(command[1]):
                    print("Pigeon not found or dead, try another pigeon")
                    return None
                self.renamePigeon(command[1], command[2])

            case "pass":
                self.update()
                print(self.info())

            case "help" | "h":
                print(self.help)

            case "clear":
                clearCMD()

            case "quit":
                return 0

            case _:
                print("Command Not Found")
