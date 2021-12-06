from json import load

class World:
    def __init__(self, savename:str, worldname:str, isDebugOn:bool=False):
        self.savename = savename
        self.worldname = worldname

        self.isDebugOn = isDebugOn

        self.year = 0
        self.month = 1

        self.wealth = 50

        self.randomNames = load(open("../input/pigeonNames.json", "r"))
        self.help = open("../input/help.txt", "r").read()
        self.genes = load(open("../input/genetics.json"))["geneBlocks"]
        self.geneValues = ["fluff", "speed", "size"]
        self.alleles = load(open("../input/genetics.json"))["possibleGenes"]

        self.species = dict() # A dictionary with all species
        self.cares = dict() # A dictionary with all cares
        self.arenas = dict() # A dictionary with all arenas

    def updateTime(self):
        self.month += 1

        if 12 < self.month:
            self.month = 1
            self.year += 1

    def command(self, command):
        command = command.lower().split()

        match command[0]:

            case "help" | "h" | "?":
                print(self.help)

            case "quit" | "q":
                raise EOFError

            case _:
                print("Command not found")
