from pigeon import *
from common import *
from random import getrandbits, randint

class daycare:
    def __init__(self, name):
        self.name = name

        self.month = 1

        self.wealth = 50

        self.pigeons = dict()
        self.allPigeons = dict()

        self.breedingDifficulty = 25 #the n out of 100 chance to successfully reproduce

    def getPigeonUID(self):
        return len(self.allPigeons)

    def createPigeon(self, uid, name, sex, parents:list=None):
        newPigeon = pigeonClass(uid, name, sex, parents)
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
                "fluff": randint(3, 18),
                "speed": randint(3, 18),
                "size": randint(3, 18),
                "cost":randint(5, 15)
            }
            print("Age: %s Months\nFemale: %s\nCost: %s\nFluffiness: %s\nSize: %s\nSpeed: %s\n"%(data["age"], data["female"], data["cost"], data["fluff"], data["size"], data["speed"]))

            i = input("Do you want to buy the pigeon?(Yes(y)/No(n)/Abort(a)) ")
            i = i.lower()

            print("\n")

            if i == "n":
                continue

            elif i == "y":
                if self.wealth < data["cost"]:
                    print("You have not enought money to buy this pigeon!")
                    j = input("Do you want to look for another pigeon(Yes(y)/No(n)) ")
                    if j == "n":
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
        answer = input("You can sell the pigeon for " + str(price) + ", do you accept? ((Yes(y)/No(n))")
        answer = answer.lower()

        if answer == "y":
            self.death(self.pigeons[pigeonUID])
            print("Pigeon sold!")
        else:
            print("Okay, than not")

    def reproduce(self, parents:list, numberOfChildren:int):
        for i in range(numberOfChildren):
            uid = self.getPigeonUID()
            child = self.createPigeon(uid, "Pigeon " + str(uid), bool(getrandbits(1)), parents)
            childGenetics = self.genetics(parents)
            child.fluffiness = childGenetics["fluff"]
            child.speed = childGenetics["speed"]
            child.size = childGenetics["size"]

            for parent in parents: #Supports more than two parents!
                parent.addChild(child)
                parent.timesBreed += 1

    def breed(self, male, female):
        timesBreed = [female.timesBreed, male.timesBreed]
        pigeons = [male, female]
        mod = 0

        for value in timesBreed:
            if value == 0:
                mod += 1
                break

            mod += 1 / value
        for pigeon in pigeons:
            pigeon.didAct = True
            pass

        if randint(0, 100) < self.breedingDifficulty * mod:
            self.reproduce(pigeons, 2)

            return 0

        return 1

    def death(self, target):
        del self.pigeons[str(target.uid)]
        target.isAlive = False

    def update(self):
        self.month += 1

        for pigeon in self.pigeons:
            pigeon = self.pigeons[str(pigeon)]
            pigeon.age += 1
            pigeon.didAct = False

    def info(self):
        infoString = ("Daycare Name: " + self.name + "\n" +
        "Month: " + str(self.month))
        infoString += "\nPigeons:"
        if isNotEmpty(self.pigeons):
            infoString += "\n"
            for pigeonKey in self.pigeons.keys():
                pigeon = self.pigeons[pigeonKey]
                infoString += "UID: %s; Name: %s; Female: %s; DidAct: %s \n"%(pigeon.uid, pigeon.name, pigeon.isFemale, pigeon.didAct)
        else:
            infoString += "\nNone"
        return infoString

    def renamePigeon(self, pigeonUID, name):
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
        listOfPigeons = list()
        for pigeonKey in self.pigeons:
            selectedPigeon = self.pigeons[pigeonKey]
            if selectedPigeon.didAct == True:
                listOfPigeons.append(selectedPigeon)
        return listOfPigeons

    def didNotActList(self):
        listOfPigeons = list()
        for pigeonKey in self.pigeons:
            selectedPigeon = self.pigeons[pigeonKey]
            if selectedPigeon.didAct == False:
                listOfPigeons.append(selectedPigeon)
        return listOfPigeons

    def genetics(self, pigeons):
        fluffiness = 0
        speed = 0
        size = 0
        for currentPigeon in pigeons:
            fluffiness += currentPigeon.fluffiness
            speed += currentPigeon.speed
            size += currentPigeon.size

        fluffiness = int(fluffiness / len(pigeons))
        speed = int(speed / len(pigeons))
        size = int(size / len(pigeons))

        return {"fluff":fluffiness, "speed":speed, "size":size}

    def do(self, command):
        command = command.lower()

        if command == "breed":
            if isEmpty(self.didNotActList()):
                print("There are no pigeons left that can breed this month, either end this month or do something else.")
                return None
                pass

            while True:
                pigeonA = input("Pick a male:")
                confirm = input("You sure you want to select " + str(pigeonA) +"? (y/n)")
                if confirm.lower() == "n":
                    continue

                try:
                    pigeonA = self.pigeons[str(pigeonA)]
                except KeyError:
                    print("Pigeon not found")
                    continue

                if pigeonA.isFemale == False:
                    break
                elif pigeonA.didAct == True:
                    print("Your targeted pigeon already breed this month")
                    continue
                else:
                    print("You targeted a female pigeon, please pick a male pigeon")
                    continue

            while True:
                pigeonB = input("Pick a female:")
                confirm = input("You sure you want to select " + str(pigeonB) +"?(y/n)")
                if confirm == "n":
                    continue

                try:
                    pigeonB = self.pigeons[str(pigeonB)]
                except KeyError:
                    print("Pigeon not found")
                    continue

                if pigeonB.isFemale == True:
                    break
                elif pigeonB.didAct == True:
                    print("Your targeted pigeon already breed this month")
                    continue
                else:
                    print("You targeted a male pigeon, please pick a female pigeon")
                    continue

            r = self.breed(pigeonA, pigeonB)
            if r == 0:
                print("Success!")
            else:
                print("Failure")

        elif command == "kill":
            pass

        elif command == "show":
            pigeonID = input("What pigeon do you want to  see? ")
            try:
                print(self.allPigeons[str(pigeonID)].show())
            except KeyError:
                print("Pigeon not found")

        elif command == "quit":
            return 0

        elif command == "info":
            print(self.info())

        elif command == "buy":
            self.buyPigeon()

        elif command == "sell":
            pigeonUID = input("Which pigeon do you want to sell? ")
            if self.isValidPigeon(pigeonUID):
                self.sellPigeon(pigeonUID)
            else:
                print("Pick another pigeon")

        elif command == "rename":
            pigeonUID = str(input("Which pigeon do you want to rename? "))
            newName = input("How should the pigeon be called? ")

            if self.isValidPigeon(pigeonUID):
                self.renamePigeon(pigeonUID, newName)
            else:
                print("Pigeon not found or dead, try another pigeon")

        elif command == "end month":
            self.update()
            print(self.info())

        elif command == "help" or command == "h":
            #Update Help Menu
            print("HELP MENU \nLIST OF COMMANDS: \n\thelp - Calls this menu \n\tshow - Shows you a pigeon of your choice \n\tbreed - Allows you to breed two pigeons \n\tbuy - gives you a random pigeon to buy \n\tsell - allows you to sell a pigeon \n\trename - allows you to rename a pigeon \n\tend month - ends month \n\tquit - Ends the game")

        elif command == "clear":
            clearCMD()

        else:
            print("Command Not Found")
