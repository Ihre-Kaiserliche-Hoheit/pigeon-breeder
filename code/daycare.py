from creature import *
from common import *
from random import getrandbits, randint

class daycare:
    def __init__(self, name):
        self.name = name

        self.month = 1

        self.wealth = 5

        self.creatures = dict()
        self.historicCreatures = dict()

        self.breedingDifficulty = 25

    def getCreatureUID(self):
        return len(self.historicCreatures)

    def createCreature(self, uid, name, sex, parents:list=None):
        newCreature = creature(uid, name, sex, parents)
        self.historicCreatures[str(newCreature.uid)] = newCreature
        self.creatures[str(newCreature.uid)] = newCreature

        return newCreature

    def generateRandomCreature(self):
        randomCreature = self.createCreature(self.getCreatureUID(), "Randy", bool(getrandbits(1)))

        return randomCreature

    def buyPigeon(self):
        while True:
            data = {
                "age":randint(6, 72),
                "female":bool(getrandbits(1)),
                "cost":randint(5, 15)
            }
            print("Age: %s Months\nFemale: %s\nCost: %s\n"%(data["age"], data["female"], data["cost"]))

            i = input("Do you want to buy the pigeon?(y/n/a)\n")
            i = i.lower()

            if i == "n":
                continue
            elif i == "y":
                if self.wealth < data["cost"]:
                    print("You have not enought money to buy this pigeon!")
                    j = input("Do you want to look for another pigeon(y/n)\n")
                    if j == "n":
                        break
                    continue
                uid = self.getCreatureUID()
                pigeon = self.createCreature(uid, "Pigeon " + str(uid), data["female"])
                pigeon.age = data["age"]
                break
            elif i == "a":
                break

    def sellPigeon(self, pigeon):
        #Code to sell pigeons goes here
        pass

    def reproduce(self, parents:list, numberOfChildren:int):
        for i in range(numberOfChildren):
            uid = self.getCreatureUID()
            child = self.createCreature(uid, "Pigeon " + str(uid), bool(getrandbits(1)), parents)

            for parent in parents: #Supports more than two parents!
                parent.addChild(child)
                parent.timesBreed += 1

    def breed(self, male, female):
        tB = [female.timesBreed, male.timesBreed]
        mod = 0

        for value in tB:
            if value == 0:
                mod += 1
                break

            mod += 1 / value

        if randint(0, 100) < self.breedingDifficulty * mod:
            self.reproduce([male, female], 2)

            return 0

        return 1

    def death(self, target):
        del self.creatures[str(target.uid)]
        target.isAlive = False

    def update(self):
        self.month += 1

        for pigeon in self.creatures:
            pigeon = self.creatures[str(pigeon)]
            pigeon.age += 1

    def info(self):
        infoString = ("Daycare Name: " + self.name + "\n" +
        "Month: " + str(self.month))

        return infoString

    def showList(self):
        for key in self.creatures.keys():
            print(key)

    def do(self, command):
        command = command.lower()

        if command == "breed":
            while True:
                pigeonA = input("Pick a male:")
                confirm = input("You sure you want to select " + str(pigeonA) +"? (y/n)")
                if confirm.lower() == "n":
                    continue

                try:
                    pigeonA = self.creatures[str(pigeonA)]
                except KeyError:
                    print("Pigeon not found")
                    continue

                if pigeonA.isFemale == False:
                    break
                else:
                    print("You targeted a female pigeon, please pick a male pigeon")
                    continue

            while True:
                pigeonB = input("Pick a male:")
                confirm = input("You sure you want to select " + str(pigeonB) +"?")
                if confirm == "n":
                    continue

                try:
                    pigeonB = self.creatures[str(pigeonB)]
                except KeyError:
                    print("Pigeon not found")
                    continue

                if pigeonB.isFemale == True:
                    break
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
                print(self.historicCreatures[str(pigeonID)].show())
            except KeyError:
                print("Pigeon not found")

        elif command == "quit":
            return 0

        elif command == "info":
            print(self.info())

        elif command == "buy":

            pass

        elif command == "end month":
            self.update()
            print(self.info())

        elif command == "help":
            print("HELP MENU")
            print("LIST OF COMMANDS:")
            print("help - Calls this menu")
            print("show - Shows you a pigeon of your choice")
            print("breed - Allows you to breed two pigeons")
            print("kill - kills the pigeon")
            print("quit - Ends the game")

        else:
            print("Command Not Found")
